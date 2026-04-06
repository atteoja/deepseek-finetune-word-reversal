# deepseek-finetune-word-reversal
Fine-tuning DeepSeek-R1 to reverse words.

## Instructions

### Data

- Define a new `data/` folder, where you should give a .txt file such as `words.txt`. This file contains words used to train the model.
- Arguments of `generate_data.py` can be used to modify the dataset generation for the task.
- By default, the dataset to be used will be stored in a `reverse_dataset.json` file under `data/`.

### Execution

- Once the `.json` dataset exists, the notebook can be run top-down to fine-tune the model.
