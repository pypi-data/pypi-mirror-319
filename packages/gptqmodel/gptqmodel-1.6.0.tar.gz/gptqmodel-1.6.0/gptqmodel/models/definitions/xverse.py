from ..base import BaseGPTQModel


class XverseGPTQ(BaseGPTQModel):
    require_pkgs_version = ["transformers<=4.38.2", "tokenizers<=0.15.2"]
    base_modules = ["model.embed_tokens", "model.norm"]

    layers_node = "model.layers"
    layer_type = "XverseDecoderLayer"
    layer_modules = [
        ["self_attn.k_proj", "self_attn.v_proj", "self_attn.q_proj"],
        ["self_attn.o_proj"],
        ["mlp.up_proj", "mlp.gate_proj"],
        ["mlp.down_proj"],
    ]
