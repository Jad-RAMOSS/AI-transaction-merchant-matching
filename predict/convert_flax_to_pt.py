# convert_flax_to_pt.py

from transformers import (
    FlaxBertForSequenceClassification,
    BertConfig,
    BertForSequenceClassification,
)
from transformers.modeling_flax_utils import convert_flax_state_dict_to_pytorch
import sys

def convert_flax_to_pt(model_dir: str):
    # 1) Load the Flax model
    flax_model = FlaxBertForSequenceClassification.from_pretrained(model_dir)
    # 2) Load its config
    config = BertConfig.from_pretrained(model_dir)
    # 3) Create a new PyTorch model
    pt_model = BertForSequenceClassification(config)
    # 4) Convert Flax params → PyTorch state dict
    pt_state = convert_flax_state_dict_to_pytorch(flax_model.params)
    pt_model.load_state_dict(pt_state)
    # 5) Save a pytorch_model.bin in the same folder
    pt_model.save_pretrained(model_dir)
    print(f"✅ Saved PyTorch checkpoint to {model_dir}/pytorch_model.bin")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_flax_to_pt.py /path/to/saved_model")
        sys.exit(1)
    convert_flax_to_pt(sys.argv[1])
