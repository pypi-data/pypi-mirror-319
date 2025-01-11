# Custom Iterable Dataset

A Python package for wrapping iterable datasets to be used with Hugging Face's `SFTTrainer`.
Just pass your iterable dataset to wrapper.

## Installation

```bash
pip install custom_iterable_dataset
```

## Usage

```python

from custom_iterable_dataset import CustomIterableDataset
from torch.utils.data import IterableDataset

# Example usage
class MyIterableDataset(IterableDataset):
    def __iter__(self):
        yield {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}

my_dataset = MyIterableDataset()
my_dataset_len = 1000
custom_dataset = CustomIterableDataset(my_dataset,my_dataset_len)

# Pass custom_dataset to SFTTrainer

```
---



