# MATS SAE Training
This is a quick-and-dirty codebase for training SAEs that we put together
so MATS 5.0 Scholars under Neel Nanda could do cool projects in their research sprint.
It prioritizes development speed over structure.

## Set Up

```

conda create --name mats_sae_training python=3.11 -y
conda activate mats_sae_training
pip install -r requirements.txt

```

## Learning

This codebase isn't currently prioritising docs, but you can work throught the 
copy of Callum McDougall's [tutorial](https://www.lesswrong.com/posts/LnHowHgmrMbWtpkxx/intro-to-superposition-and-sparse-autoencoders-colab) 
if you want to get more familiar with the subject
matter before engaging.

## Training a Sparse Autoencoder on a Language Model

(warning, config may go out of date!)

```python
import torch

from sae_training.config import LanguageModelSAERunnerConfig
from sae_training.lm_runner import language_model_sae_runner

cfg = LanguageModelSAERunnerConfig(

    # Data Generating Function (Model + Training Distibuion)
    model_name = "gelu-2l",
    hook_point = "blocks.0.hook_mlp_out",
    hook_point_layer = 0,
    d_in = 512,
    dataset_path = "NeelNanda/c4-tokenized-2b",
    is_dataset_tokenized=True,
    
    # SAE Parameters
    expansion_factor = 64, # determines the dimension of the SAE.
    
    # Training Parameters
    lr = 1e-4,
    l1_coefficient = 3e-4,
    train_batch_size = 4096,
    context_size = 128,
    
    # Activation Store Parameters
    n_batches_in_buffer = 24,
    total_training_tokens = 5_000_00 * 100, # 15 minutes on an A100
    store_batch_size = 32,
    
    # Resampling protocol
    feature_sampling_method = 'l2',
    feature_sampling_window = 1000, # would fire ~5 times on 500 million tokens
    feature_reinit_scale = 0.2,
    dead_feature_threshold = 1e-8,
    
    # WANDB
    log_to_wandb = True,
    wandb_project= "mats_sae_training_language_models",
    wandb_entity = None,
    
    # Misc
    device = "cuda",
    seed = 42,
    n_checkpoints = 5,
    checkpoint_path = "checkpoints",
    dtype = torch.float32,
    )

sparse_autoencoder = language_model_sae_runner(cfg)

```


## Loading a Pretrained Language Model 

```python
from sae_training.utils import LMSparseAutoencoderSessionloader

path ="path/to/sparse_autoencoder.pt"
model, sparse_autoencoder, activations_loader = LMSparseAutoencoderSessionloader.load_session_from_pretrained(
    path
)

```
## Tutorials

See the `tutorials` folder for the following tutorials:
- `exercises_and_solutions.ipynb`: A copy of Callum McDougall's SAE exercises which provide background knowledge on this codebase.
- `evaluating_your_sae.ipynb`: A quick/dirty notebook showing how to check L0 and Prediction loss with your SAE, as well as showing how to generate interactive dashboards using Callum's reporduction of [Anthropics interface](https://transformer-circuits.pub/2023/monosemantic-features#setup-interface). 

## Example Dashboard

WandB Dashboards provide lots of useful insights while training SAE's. Here's a screenshot from one training run. 

![screenshot](dashboard_screenshot.png)


## Example Output

Here's one feature we found in the residual stream of Layer 10 of GPT-2 Small:

![alt text](readme_screenshot_predict_pronoun_feature.png). Open `gpt2_resid_pre10_predict_pronoun_feature.html` in your browser to interact with the dashboard (WIP).

Note, probably this feature could split into more mono-semantic features in a larger SAE that had been trained for longer. (this was was only about 49152 features trained on 10M tokens from OpenWebText).


## Citations and References:

Research:
- [Towards Monosemanticy](https://transformer-circuits.pub/2023/monosemantic-features)
- [Sparse Autoencoders Find Highly Interpretable Features in Language Model](https://arxiv.org/abs/2309.08600)



Reference Implementations:
- [Neel Nanda](https://github.com/neelnanda-io/1L-Sparse-Autoencoder)
- [AI-Safety-Foundation](https://github.com/ai-safety-foundation/sparse_autoencoder).
- [Arthur Conmy](https://github.com/ArthurConmy/sae).
- [Callum McDougall](https://github.com/callummcdougall/sae-exercises-mats/tree/main)
