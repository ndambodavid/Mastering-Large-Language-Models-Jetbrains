# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **JetBrains Academy "Mastering Large Language Models"** course — a study-mode project where students implement LLM-related code inside `task.py` files that contain `# TODO` markers. The six modules build progressively: NLP basics → language modeling → LLaMA from scratch → fine-tuning → RAG → Anki card generation.

## Environment Setup

```bash
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r FineTuning/requirements.txt  # extra FineTuning deps
```

Python version: **3.12**. Two private packages are used across the course: `tools-basics` and `custom-helpers`.

## Running Tests

Each task with automated tests has a `tests/test_task.py`. Run tests for a specific task:

```bash
pytest NLPBasics/task02_tokenization/tests/
pytest FineTuning/task3_dataset/tests/
pytest RAG/task2_dataset/tests/
# etc.
```

Run all tests:
```bash
pytest
```

## Running Tasks

Most tasks can be executed directly as scripts:

```bash
python NLPBasics/task02_tokenization/task.py
```

Some tasks have dedicated runners:

```bash
python FineTuning/task2_prompting/run.py
python RAG/task4_vector_storage/run.py

# FineTuning PEFT — trains all three methods (LoRA, IA³, Prompt Tuning)
cd FineTuning/task6_peft && bash run.sh
python FineTuning/task6_peft/run_eval.py
```

## Module Architecture

### NLPBasics
Sentiment classification on the Stanford IMDB dataset. Sequential pipeline: tokenization → GloVe embeddings → visualization → KNN/Naive Bayes/Logistic Regression classifiers. Config at `NLPBasics/conf.yaml`; `envvars.py` exposes `LessonEnv.ROOT_DIRECTORY` and `LessonEnv.CONF_PATH` used by every task in the lesson.

### LanguageModeling
N-gram models, text generation, perplexity, Laplace smoothing, and then a full PyTorch RNN trained on ArXiv abstracts. Config at `LanguageModeling/conf.yaml`. Data must be downloaded first via `LanguageModeling/task01_ngrams/download_data.py`.

### MinLlama
Implements LLaMA2 architecture from scratch in PyTorch. Key components to implement are spread across sub-packages:
- `RoPE/task.py` — Rotary Position Embeddings
- `Llama/task.py` — `RMSNorm`, `Attention.compute_query_key_value_scores`, `LlamaLayer.forward`
- `Optimizer/` — custom optimizer
- `HelperCode/` — `base_llama.py`, `config.py`, `tokenizer.py`, `utils.py` (pre-written infrastructure)
- `Running/main.py` — entry point for running the trained model

### FineTuning
Fine-tunes `unsloth/Llama-3.2-1B-Instruct` on a C1-vocabulary word-definition task. Pipeline: prompting → dataset building → helper utilities → grid search trainer → PEFT methods (LoRA / IA³ / Prompt Tuning). Config at `FineTuning/conf.yaml`. Experiments are saved under `FineTuning/experiments/`.

### RAG
Trains a bi-encoder (based on `NovaSearch/stella_en_400M_v5`) for retrieval-augmented generation over WordNet definitions. Pipeline: dataset → training → vector store → inference. Config at `RAG/config.yaml`.

### GenAnkiCards
Uses the OpenAI API to generate flashcards (text + image + audio), then uploads them to Anki via AnkiConnect.

## Config Pattern

All lessons use `omegaconf`. Config YAMLs have `root_dir: ???` which is resolved at runtime by the `LessonEnv` class (or `custom_helpers.add_root_to_pythonpath`). You generally do not need to edit the YAML files; the path resolution is automatic when running scripts from within the correct directory.

## Task Pattern

Every `task.py` file is where student code goes. Stubs contain:
- `# TODO: implement ...` for short completions
- `pass # TODO: YOUR CODE HERE` for full method bodies

Supporting infrastructure (data loading, config, helpers) lives in the lesson-level files and `HelperCode/` directories — do not modify those unless fixing a bug in the scaffolding.
