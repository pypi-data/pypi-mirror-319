#include <flashinfer/attention_impl.cuh>

namespace flashinfer {

using ParamsT = BatchPrefillRaggedParams<half, half, half, int32_t>;

using AttentionVariant1 = ComposedAttention<ParamsT, get_variant_code(
    true, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/false, /*use_alibi_bias=*/false)>;

template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<128, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant1>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        
template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<64, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant1>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        
template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<16, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant1>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        

using AttentionVariant2 = ComposedAttention<ParamsT, get_variant_code(
    true, /*use_sliding_window=*/true, /*use_logits_soft_cap=*/true, /*use_alibi_bias=*/false)>;

template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<128, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant2>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        
template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<64, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant2>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        
template cudaError_t BatchPrefillWithRaggedKVCacheDispatched<16, 256, PosEncodingMode::kNone, 0, MaskMode::kCustom, AttentionVariant2>(
    ParamsT params,
    half* tmp_v,
    float* tmp_s, cudaStream_t stream);
        

}
    