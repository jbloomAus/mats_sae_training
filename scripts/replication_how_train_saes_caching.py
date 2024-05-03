import os
import shutil

import torch

from sae_lens.training.cache_activations_runner import CacheActivationsRunner

# from pathlib import Path
from sae_lens.training.config import CacheActivationsRunnerConfig

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print("Using device:", device)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

total_training_steps = 2_000
batch_size = 4096
total_training_tokens = total_training_steps * batch_size
print(f"Total Training Tokens: {total_training_tokens}")

lr_warm_up_steps = 0
lr_decay_steps = 200_000 // 5  # 20% of training steps.
print(f"lr_decay_steps: {lr_decay_steps}")
l1_warmup_steps = 200_000 // 20  # 5% of training steps.
print(f"l1_warmup_steps: {l1_warmup_steps}")

new_cached_activations_path = "/Volumes/T7 Shield/activations/gelu_1l_test"

# If the directory exists, delete it.
if os.path.exists(new_cached_activations_path):
    shutil.rmtree(new_cached_activations_path)

torch.mps.empty_cache()

cfg = CacheActivationsRunnerConfig(
    new_cached_activations_path=new_cached_activations_path,
    # Pick a tiny model to make this easier.
    model_name="gelu-1l",
    ## MLP Layer 0 ##
    hook_point="blocks.0.hook_mlp_out",
    hook_point_layer=0,
    d_in=512,
    dataset_path="NeelNanda/c4-tokenized-2b",
    context_size=1024,
    is_dataset_tokenized=True,
    prepend_bos=True,
    training_tokens=total_training_tokens,  # For initial testing I think this is a good number.
    train_batch_size=4096,
    # buffer details
    n_batches_in_buffer=32,
    store_batch_size=16,
    normalize_activations=False,
    #
    shuffle_every_n_buffers=8,
    n_shuffles_with_last_section=1,
    n_shuffles_in_entire_dir=1,
    n_shuffles_final=1,
    # Misc
    device=device,
    seed=42,
    dtype=torch.float32,
)
# look at the next cell to see some instruction for what to do while this is running.
CacheActivationsRunner(cfg).run()
