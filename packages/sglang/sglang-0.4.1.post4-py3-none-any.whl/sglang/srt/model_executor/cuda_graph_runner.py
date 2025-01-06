# Copyright 2023-2024 SGLang Team
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Run the model with cuda graph and torch.compile."""

from __future__ import annotations

import bisect
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable

import torch
import tqdm
from vllm.distributed import get_tensor_model_parallel_rank
from vllm.distributed.parallel_state import graph_capture
from vllm.model_executor.custom_op import CustomOp

from sglang.srt.layers.logits_processor import LogitsProcessorOutput
from sglang.srt.layers.moe.fused_moe_native import fused_moe_forward_native
from sglang.srt.layers.torchao_utils import save_gemlite_cache
from sglang.srt.model_executor.forward_batch_info import (
    CaptureHiddenMode,
    ForwardBatch,
    ForwardMode,
)
from sglang.srt.utils import monkey_patch_vllm_all_gather

if TYPE_CHECKING:
    from sglang.srt.model_executor.model_runner import ModelRunner


def _to_torch(model: torch.nn.Module, reverse: bool, batch_size: int):
    for sub in model._modules.values():
        if isinstance(sub, CustomOp):
            if reverse:
                sub._forward_method = sub.forward_cuda
                setattr(sub, "is_torch_compile", False)
            else:
                # NOTE: Temporarily workaround MoE
                if "FusedMoE" in sub.__class__.__name__:
                    if batch_size == 1:
                        # The performance of torch.compile on this layer is not always good when bs > 1,
                        # so we decide to only use torch.compile when bs =1
                        sub._forward_method = fused_moe_forward_native
                else:
                    sub._forward_method = sub.forward_native
                setattr(sub, "is_torch_compile", True)
        if isinstance(sub, torch.nn.Module):
            _to_torch(sub, reverse, batch_size)


@contextmanager
def patch_model(
    model: torch.nn.Module,
    enable_compile: bool,
    batch_size: int,
    tp_group: "GroupCoordinator",
):
    """Patch the model to make it compatible with with torch.compile"""
    backup_ca_comm = None

    try:
        if enable_compile:
            _to_torch(model, reverse=False, batch_size=batch_size)
            monkey_patch_vllm_all_gather()
            backup_ca_comm = tp_group.ca_comm
            # Use custom-allreduce here.
            # We found the custom allreduce is much faster than the built-in allreduce in torch,
            # even with ENABLE_INTRA_NODE_COMM=1.
            # tp_group.ca_comm = None
            yield torch.compile(
                torch.no_grad()(model.forward),
                mode="max-autotune-no-cudagraphs",
                dynamic=False,
            )
        else:
            yield model.forward
    finally:
        if enable_compile:
            _to_torch(model, reverse=True, batch_size=batch_size)
            monkey_patch_vllm_all_gather(reverse=True)
            tp_group.ca_comm = backup_ca_comm


def set_torch_compile_config():
    import torch._dynamo.config
    import torch._inductor.config

    torch._inductor.config.coordinate_descent_tuning = True
    torch._inductor.config.triton.unique_kernel_names = True
    torch._inductor.config.fx_graph_cache = True  # Experimental feature to reduce compilation times, will be on by default in future

    # FIXME: tmp workaround
    torch._dynamo.config.accumulated_cache_size_limit = 1024
    if hasattr(torch._dynamo.config, "cache_size_limit"):
        torch._dynamo.config.cache_size_limit = 1024


class CudaGraphRunner:
    """A CudaGraphRunner runs the forward pass of a model with cuda graph and torch.compile."""

    def __init__(self, model_runner: "ModelRunner"):
        # Parse args
        self.model_runner = model_runner
        self.graphs = {}
        self.input_buffers = {}
        self.output_buffers = {}
        self.flashinfer_handlers = {}
        self.graph_memory_pool = None
        self.use_torch_compile = model_runner.server_args.enable_torch_compile
        self.disable_padding = model_runner.server_args.disable_cuda_graph_padding
        self.is_encoder_decoder = self.model_runner.model_config.is_encoder_decoder
        self.enable_dp_attention = self.model_runner.server_args.enable_dp_attention
        self.tp_size = self.model_runner.tp_size

        # Batch sizes to capture
        if model_runner.server_args.disable_cuda_graph_padding:
            self.capture_bs = list(range(1, 33)) + [64, 128]
        else:
            self.capture_bs = [1, 2, 4] + [i * 8 for i in range(1, 21)]

        if max(self.capture_bs) > model_runner.req_to_token_pool.size:
            # In some case (e.g., with a small GPU or --max-running-requests), the #max-running-requests
            # is very samll. We add more values here to make sure we capture the maximum bs.
            self.capture_bs = list(
                sorted(
                    set(
                        self.capture_bs
                        + [model_runner.req_to_token_pool.size - 1]
                        + [model_runner.req_to_token_pool.size]
                    )
                )
            )

        self.capture_bs = [
            bs
            for bs in self.capture_bs
            if bs <= model_runner.req_to_token_pool.size
            and bs <= model_runner.server_args.cuda_graph_max_bs
        ]

        self.capture_forward_mode = ForwardMode.DECODE
        self.num_tokens_per_bs = 1

        if model_runner.spec_algorithm.is_eagle():
            if self.model_runner.is_draft_worker:
                self.num_tokens_per_bs = (
                    self.model_runner.server_args.speculative_eagle_topk
                )
            else:
                self.capture_forward_mode = ForwardMode.TARGET_VERIFY
                self.num_tokens_per_bs = (
                    self.model_runner.server_args.speculative_num_draft_tokens
                )

        self.compile_bs = (
            [
                bs
                for bs in self.capture_bs
                if bs <= self.model_runner.server_args.torch_compile_max_bs
            ]
            if self.use_torch_compile
            else []
        )

        # Attention backend
        self.max_bs = max(self.capture_bs)
        self.max_num_token = self.max_bs * self.num_tokens_per_bs
        self.model_runner.attn_backend.init_cuda_graph_state(self.max_num_token)
        self.seq_len_fill_value = (
            self.model_runner.attn_backend.get_cuda_graph_seq_len_fill_value()
        )

        # FIXME(lsyin): leave it here for now, I don't know whether it is necessary
        self.encoder_len_fill_value = 0

        if self.use_torch_compile:
            set_torch_compile_config()

        # Common inputs
        with torch.device("cuda"):
            self.input_ids = torch.zeros((self.max_num_token,), dtype=torch.int32)
            self.req_pool_indices = torch.zeros((self.max_bs,), dtype=torch.int32)
            self.seq_lens = torch.full(
                (self.max_bs,), self.seq_len_fill_value, dtype=torch.int32
            )
            self.out_cache_loc = torch.zeros((self.max_num_token,), dtype=torch.int32)
            self.positions = torch.zeros((self.max_num_token,), dtype=torch.int64)
            self.mrope_positions = torch.zeros((3, self.max_bs), dtype=torch.int32)

            # Speculative_inference
            if model_runner.spec_algorithm.is_eagle():
                self.hidden_states = torch.zeros(
                    (self.max_num_token, self.model_runner.model_config.hidden_size),
                    dtype=self.model_runner.dtype,
                )

            if self.is_encoder_decoder:
                # NOTE: encoder_lens can influence the full_text_row_masked_out_mask tensor when doing mixed batch
                self.encoder_lens = torch.full(
                    (self.max_bs,), self.encoder_len_fill_value, dtype=torch.int32
                )
            else:
                self.encoder_lens = None

            if self.enable_dp_attention:
                self.gathered_buffer = torch.zeros(
                    (
                        self.max_bs * self.tp_size,
                        self.model_runner.model_config.hidden_size,
                    ),
                    dtype=self.model_runner.dtype,
                )

        # Capture
        try:
            with self.model_capture_mode():
                self.capture()
        except RuntimeError as e:
            raise Exception(
                f"Capture cuda graph failed: {e}\n"
                "Possible solutions:\n"
                "1. disable cuda graph by --disable-cuda-graph\n"
                "2. set --mem-fraction-static to a smaller value (e.g., 0.8 or 0.7)\n"
                "3. disable torch compile by not using --enable-torch-compile\n"
                "Open an issue on GitHub https://github.com/sgl-project/sglang/issues/new/choose \n"
            )

    @contextmanager
    def model_capture_mode(self):
        if hasattr(self.model_runner.model, "capture_mode"):
            self.model_runner.model.capture_mode = True

        yield

        if hasattr(self.model_runner.model, "capture_mode"):
            self.model_runner.model.capture_mode = False

    def can_run(self, forward_batch: ForwardBatch):
        if self.enable_dp_attention:
            min_num_tokens, max_num_tokens = min(forward_batch.global_num_tokens), max(
                forward_batch.global_num_tokens
            )
            is_bs_supported = forward_batch.can_run_dp_cuda_graph and (
                (min_num_tokens == max_num_tokens and max_num_tokens in self.graphs)
                if self.disable_padding
                else max_num_tokens <= self.max_bs
            )
        else:
            is_bs_supported = (
                forward_batch.batch_size in self.graphs
                if self.disable_padding
                else forward_batch.batch_size <= self.max_bs
            )

        # NOTE: cuda graph cannot handle mixed batch (encoder_len = 0)
        # If mixed batch cannot be supported, then encoder_lens can be removed in cuda graph
        # because the full_text_row_masked_out_mask tensor will always be ones
        is_encoder_lens_supported = (
            torch.all(forward_batch.encoder_lens > 0)
            if self.is_encoder_decoder
            else True
        )
        return is_bs_supported and is_encoder_lens_supported

    def capture(self):
        with graph_capture() as graph_capture_context:
            self.stream = graph_capture_context.stream
            capture_range = (
                tqdm.tqdm(self.capture_bs)
                if get_tensor_model_parallel_rank() == 0
                else self.capture_bs
            )
            for bs in capture_range:
                with patch_model(
                    self.model_runner.model,
                    bs in self.compile_bs,
                    bs,
                    self.model_runner.tp_group,
                ) as forward:
                    (
                        graph,
                        output_buffers,
                    ) = self.capture_one_batch_size(bs, forward)
                    self.graphs[bs] = graph
                    self.output_buffers[bs] = output_buffers

                # Save gemlite cache after each capture
                save_gemlite_cache()

    def capture_one_batch_size(self, bs: int, forward: Callable):
        graph = torch.cuda.CUDAGraph()
        stream = self.stream
        num_tokens = bs * self.num_tokens_per_bs

        # Common inputs
        input_ids = self.input_ids[:num_tokens]
        req_pool_indices = self.req_pool_indices[:bs]
        seq_lens = self.seq_lens[:bs]
        out_cache_loc = self.out_cache_loc[:num_tokens]
        positions = self.positions[:num_tokens]
        if self.is_encoder_decoder:
            encoder_lens = self.encoder_lens[:bs]
        else:
            encoder_lens = None
        mrope_positions = self.mrope_positions[:, :bs]

        if self.enable_dp_attention:
            global_num_tokens = [bs] * self.tp_size
            gathered_buffer = self.gathered_buffer[: bs * self.tp_size]
        else:
            global_num_tokens = None
            gathered_buffer = None

        forward_batch = ForwardBatch(
            forward_mode=self.capture_forward_mode,
            batch_size=bs,
            input_ids=input_ids,
            req_pool_indices=req_pool_indices,
            seq_lens=seq_lens,
            req_to_token_pool=self.model_runner.req_to_token_pool,
            token_to_kv_pool=self.model_runner.token_to_kv_pool,
            attn_backend=self.model_runner.attn_backend,
            out_cache_loc=out_cache_loc,
            seq_lens_sum=seq_lens.sum(),
            encoder_lens=encoder_lens,
            return_logprob=False,
            top_logprobs_nums=[0] * bs,
            positions=positions,
            global_num_tokens=global_num_tokens,
            mrope_positions=mrope_positions,
            gathered_buffer=gathered_buffer,
            spec_algorithm=self.model_runner.spec_algorithm,
            spec_info=self.get_spec_info(num_tokens, positions),
        )

        # Attention backend
        self.model_runner.attn_backend.init_forward_metadata_capture_cuda_graph(
            bs,
            num_tokens,
            req_pool_indices,
            seq_lens,
            encoder_lens,
            forward_batch.forward_mode,
            forward_batch.spec_info,
        )

        # Run and capture
        def run_once():
            logits_output = forward(input_ids, forward_batch.positions, forward_batch)
            return logits_output.next_token_logits, logits_output.hidden_states

        for _ in range(2):
            torch.cuda.synchronize()
            self.model_runner.tp_group.barrier()

            run_once()

            torch.cuda.synchronize()
            self.model_runner.tp_group.barrier()

        torch.cuda.synchronize()
        self.model_runner.tp_group.barrier()

        with torch.cuda.graph(graph, pool=self.graph_memory_pool, stream=stream):
            out = run_once()

        torch.cuda.synchronize()
        self.model_runner.tp_group.barrier()

        self.graph_memory_pool = graph.pool()
        return graph, out

    def replay(self, forward_batch: ForwardBatch):
        assert forward_batch.out_cache_loc is not None
        raw_bs = forward_batch.batch_size
        raw_num_token = raw_bs * self.num_tokens_per_bs

        # Pad
        if self.enable_dp_attention:
            index = bisect.bisect_left(
                self.capture_bs, max(forward_batch.global_num_tokens)
            )
        else:
            index = bisect.bisect_left(self.capture_bs, raw_bs)
        bs = self.capture_bs[index]
        if bs != raw_bs:
            self.seq_lens.fill_(1)
            self.out_cache_loc.zero_()

        # Common inputs
        self.input_ids[:raw_num_token].copy_(forward_batch.input_ids)
        self.req_pool_indices[:raw_bs].copy_(forward_batch.req_pool_indices)
        self.seq_lens[:raw_bs].copy_(forward_batch.seq_lens)
        self.out_cache_loc[:raw_num_token].copy_(forward_batch.out_cache_loc)
        self.positions[:raw_num_token].copy_(forward_batch.positions)

        if self.is_encoder_decoder:
            self.encoder_lens[:raw_bs].copy_(forward_batch.encoder_lens)
        if forward_batch.mrope_positions is not None:
            self.mrope_positions[:, :raw_bs].copy_(forward_batch.mrope_positions)

        if hasattr(forward_batch.spec_info, "hidden_states"):
            self.hidden_states[:raw_num_token] = forward_batch.spec_info.hidden_states

        # Attention backend
        self.model_runner.attn_backend.init_forward_metadata_replay_cuda_graph(
            bs,
            self.req_pool_indices,
            self.seq_lens,
            forward_batch.seq_lens_sum + (bs - raw_bs),
            self.encoder_lens,
            forward_batch.forward_mode,
            forward_batch.spec_info,
        )

        # Replay
        self.graphs[bs].replay()
        next_token_logits, hidden_states = self.output_buffers[bs]

        logits_output = LogitsProcessorOutput(
            next_token_logits=next_token_logits[:raw_num_token],
            hidden_states=(
                hidden_states[:raw_num_token] if hidden_states is not None else None
            ),
        )
        return logits_output

    def get_spec_info(self, num_tokens: int, positions: torch.Tensor):
        spec_info = None
        if self.model_runner.spec_algorithm.is_eagle():
            from sglang.srt.speculative.eagle_utils import (
                EAGLEDraftInput,
                EagleVerifyInput,
            )

            if self.model_runner.is_draft_worker:
                spec_info = EAGLEDraftInput()
                spec_info.hidden_states = self.hidden_states[:num_tokens]
                spec_info.positions = positions
                spec_info.capture_hidden_mode = CaptureHiddenMode.FULL
                spec_info.init(self.model_runner.server_args)
            else:
                spec_info = EagleVerifyInput(
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    self.model_runner.server_args.speculative_num_draft_tokens,
                )
                spec_info.custom_mask = torch.zeros(
                    (num_tokens * self.model_runner.model_config.context_len),
                    dtype=torch.bool,
                    device="cuda",
                )
                spec_info.capture_hidden_mode = CaptureHiddenMode.FULL

        return spec_info
