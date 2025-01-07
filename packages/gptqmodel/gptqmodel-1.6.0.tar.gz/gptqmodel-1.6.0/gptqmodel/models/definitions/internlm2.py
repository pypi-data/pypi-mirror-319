from ..base import BaseGPTQModel


class InternLM2GPTQ(BaseGPTQModel):

    require_pkgs_version = ["transformers<=4.44.2"]

    base_modules = ["model.tok_embeddings", "model.norm"]

    layers_node = "model.layers"
    layer_type = "InternLM2DecoderLayer"
    layer_modules = [
        ["attention.wqkv", "attention.wo"],

        ["feed_forward.w1", "feed_forward.w3"],
        ["feed_forward.w2"],
    ]
