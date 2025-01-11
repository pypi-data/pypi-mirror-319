#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = SingleDecodeParams<half, half, half>;

template cudaError_t SingleDecodeWithKVCacheDispatched<128, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp,
    cudaStream_t stream);

template cudaError_t SingleDecodeWithKVCacheDispatched<128, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    half* tmp,
    cudaStream_t stream);
}
    