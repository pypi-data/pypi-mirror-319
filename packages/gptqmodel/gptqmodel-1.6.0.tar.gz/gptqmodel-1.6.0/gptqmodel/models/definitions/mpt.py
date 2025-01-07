from ..base import BaseGPTQModel


class MPTGPTQ(BaseGPTQModel):
    base_modules = ["transformer.wte", "transformer.norm_f"]

    layers_node = "transformer.blocks"
    layer_type = "MPTBlock"
    layer_modules = [
        ["attn.Wqkv"],
        ["attn.out_proj"],
        ["ffn.up_proj"],
        ["ffn.down_proj"]
    ]
