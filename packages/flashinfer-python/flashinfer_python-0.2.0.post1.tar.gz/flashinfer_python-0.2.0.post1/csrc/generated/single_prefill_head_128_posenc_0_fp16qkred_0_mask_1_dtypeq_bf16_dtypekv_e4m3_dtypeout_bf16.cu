#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = SinglePrefillParams<nv_bfloat16, __nv_fp8_e4m3, nv_bfloat16>;

template cudaError_t SinglePrefillWithKVCacheDispatched<128, PosEncodingMode::kNone, 0, MaskMode::kCausal, ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    nv_bfloat16* tmp,
    cudaStream_t stream);

template cudaError_t SinglePrefillWithKVCacheDispatched<128, PosEncodingMode::kNone, 0, MaskMode::kCausal, ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    nv_bfloat16* tmp,
    cudaStream_t stream);

}
    