#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = BatchDecodeParams<half, __nv_fp8_e4m3, half, int32_t>;

template cudaError_t BatchDecodeWithPagedKVCacheDispatched<64, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp_v, float* tmp_s,
    cudaStream_t stream);

template cudaError_t BatchDecodeWithPagedKVCacheDispatched<64, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp_v, float* tmp_s,
    cudaStream_t stream);


using ParamsMlaT = BatchDecodeParamsMLA<half, __nv_fp8_e4m3, half, int32_t>;

template cudaError_t BatchDecodeWithPagedKVCacheDispatchedMLA<64, 8, ComposedAttention<ParamsMlaT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsMlaT params,
    half* tmp_v, float* tmp_s,
    cudaStream_t stream);
}
    