#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = SinglePrefillParams<half, half, half>;

template cudaError_t SinglePrefillWithKVCacheDispatched<64, PosEncodingMode::kNone, 0, MaskMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp,
    cudaStream_t stream);

template cudaError_t SinglePrefillWithKVCacheDispatched<64, PosEncodingMode::kNone, 0, MaskMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp,
    cudaStream_t stream);

}
    