from .._const import EXPERT_INDEX_PLACEHOLDER
from ..base import BaseGPTQModel


# Both DeepSeek-v2 and DeepSeek-v2-lite are supported in this model def
class DeepSeekV2GPTQ(BaseGPTQModel):
    # deepseek_v2 requires custom model code
    require_trust_remote_code = True

    # allow dynamic expert index for layer_modules so we don't need to write out 64 layers here
    # config.num_experts contains the actual expert count used for index
    dynamic_expert_index = "n_routed_experts"

    base_modules = ["model.embed_tokens", "model.norm"]

    layers_node = "model.layers"
    layer_type = "DeepseekV2DecoderLayer"

    # DeepSeek-V2 uses 160 experts, v2-lite is auto-switched during __init__
    layer_modules = [
        # DeepSeek-V2 and DeepSeek-V2-Lite use same model_type, but different self_attn
        # so we provide different layer_modules usage.
        # DeepSeek-V2-Lite usage
        ["self_attn.q_proj", "self_attn.kv_a_proj_with_mqa", "self_attn.kv_b_proj"],

        # DeepSeek-V2 usage, included in layer 0-59
        ["self_attn.q_a_proj", "self_attn.q_b_proj", "self_attn.kv_a_proj_with_mqa", "self_attn.kv_b_proj"],

        ["self_attn.o_proj"],

        # included in layer 0
        ["mlp.gate_proj", "mlp.up_proj"],
        ["mlp.down_proj"],

        # included in layer 1-59, uses dynamic_expert_index
        [f"mlp.experts.{EXPERT_INDEX_PLACEHOLDER}.gate_proj", f"mlp.experts.{EXPERT_INDEX_PLACEHOLDER}.up_proj"],
        [f"mlp.experts.{EXPERT_INDEX_PLACEHOLDER}.down_proj"],

        # included in layer 1-59
        ["mlp.shared_experts.gate_proj", "mlp.shared_experts.up_proj"],
        ["mlp.shared_experts.down_proj"],
    ]
