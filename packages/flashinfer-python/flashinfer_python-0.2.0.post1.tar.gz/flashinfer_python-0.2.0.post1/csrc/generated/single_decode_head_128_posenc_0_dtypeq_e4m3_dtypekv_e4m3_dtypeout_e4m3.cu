#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = SingleDecodeParams<__nv_fp8_e4m3, __nv_fp8_e4m3, __nv_fp8_e4m3>;

template cudaError_t SingleDecodeWithKVCacheDispatched<128, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    __nv_fp8_e4m3* tmp,
    cudaStream_t stream);

template cudaError_t SingleDecodeWithKVCacheDispatched<128, PosEncodingMode::kNone, ComposedAttention<ParamsT, get_variant_code(
    /*use_custom_mask=*/false, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>>(
    ParamsT params,
    __nv_fp8_e4m3* tmp,
    cudaStream_t stream);
}
    