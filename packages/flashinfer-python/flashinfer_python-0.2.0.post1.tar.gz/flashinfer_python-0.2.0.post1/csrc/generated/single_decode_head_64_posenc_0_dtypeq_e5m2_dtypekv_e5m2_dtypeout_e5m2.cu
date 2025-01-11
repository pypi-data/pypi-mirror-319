#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = SingleDecodeParams<__nv_fp8_e5m2, __nv_fp8_e5m2, __nv_fp8_e5m2>;

template cudaError_t SingleDecodeWithKVCacheDispatched<64, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    __nv_fp8_e5m2* tmp,
    cudaStream_t stream);

template cudaError_t SingleDecodeWithKVCacheDispatched<64, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    __nv_fp8_e5m2* tmp,
    cudaStream_t stream);
}
    