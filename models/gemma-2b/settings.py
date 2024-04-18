from datasets import load_dataset
from random import randrange

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model, AutoPeftModelForCausalLM

from trl import SFTTrainer

from constants import *

# The model that you want to train from the Hugging Face hub
model_id = "google/gemma-2b"
# The instruction dataset to use
dataset_name = EDITORIAL_DATASET
# Dataset split
dataset_split = "train"
# Fine-tuned model name
new_model = "gemma-2b-editorial"
# Huggingface repository
hf_model_repo = GENERATOR_MODEL_ID
# Load the entire model on the GPU 0
device_map = "auto"

################################################################################
# bitsandbytes parameters
################################################################################
# Activate 4-bit precision base model loading
use_4bit = True
# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"
# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"
# Activate nested quantization for 4-bit base models (double quantization)
use_double_nested_quant = False

################################################################################
# QLoRA parameters
################################################################################
# LoRA attention dimension
lora_r = 16
# Alpha parameter for LoRA scaling
lora_alpha = 16
# Dropout probability for LoRA layers
lora_dropout = 0.05

################################################################################
# TrainingArguments parameters
################################################################################
# Output directory where the model predictions and checkpoints will be stored
output_dir = new_model
# Number of training epochs
num_train_epochs = 2
# Enable fp16/bf16 training (set bf16 to True with an A100)
fp16 = True
bf16 = False
# Batch size per GPU for training
batch_size = 128
per_device_train_batch_size = 1
# Number of update steps to accumulate the gradients for
gradient_accumulation_steps = batch_size // per_device_train_batch_size
# Enable gradient checkpointing
gradient_checkpointing = False
# Maximum gradient normal (gradient clipping)
max_grad_norm = 0.3
# Initial learning rate (AdamW optimizer)
learning_rate = 3e-4 #1e-5
# Weight decay to apply to all layers except bias/LayerNorm weights
weight_decay = 0.001
# Optimizer to use
optim = "paged_adamw_32bit"
# Learning rate schedule
lr_scheduler_type = "constant" # "constant"
# Number of training steps (overrides num_train_epochs)
max_steps = -1
# Ratio of steps for a linear warmup (from 0 to learning rate)
warmup_ratio = 0.03
# Group sequences into batches with same length
# Saves memory and speeds up training considerably
group_by_length = False
# Save checkpoint every X updates steps
save_steps = 0
# Log every X updates steps
logging_steps = 25
# Disable tqdm
disable_tqdm = True

################################################################################
# SFTTrainer parameters
################################################################################
# Maximum sequence length to use
max_seq_length = 512 #None
# Pack multiple short examples in the same input sequence to increase efficiency
packing = True #True #False

# High-level parameters

compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_use_double_quant=use_double_nested_quant,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype
)

peft_config = LoraConfig(
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=lora_r,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
        ],
)

# Define the training arguments
args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=per_device_train_batch_size, # 6 if use_flash_attention else 4,
    gradient_accumulation_steps=gradient_accumulation_steps,
    gradient_checkpointing=gradient_checkpointing,
    optim=optim,
    #save_steps=save_steps,
    logging_steps=logging_steps,
    save_strategy="epoch",
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=fp16,
    bf16=bf16,
    max_grad_norm=max_grad_norm,
    warmup_ratio=warmup_ratio,
    #max_steps=max_steps,
    group_by_length=group_by_length,
    lr_scheduler_type=lr_scheduler_type,
    disable_tqdm=disable_tqdm,
    report_to="tensorboard",
    seed=42
)
