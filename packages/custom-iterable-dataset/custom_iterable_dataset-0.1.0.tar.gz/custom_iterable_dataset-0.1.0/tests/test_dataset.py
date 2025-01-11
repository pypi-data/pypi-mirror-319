import pytest
from torch.utils.data import Dataset
from custom_iterable_dataset.dataset import CustomDataset  # Replace with your actual package name

# Fixture for a dummy iterable dataset
@pytest.fixture
def dummy_dataset():
    class DummyIterableDataset(Dataset):
        def __init__(self, data):
            self.data = data

        def __len__(self):
            return len(self.data)

        def __getitem__(self, index):
            return self.data[index]

    # Sample data
    data = [
        {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]},
        {"input_ids": [4, 5, 6], "attention_mask": [1, 1, 1]},
        {"input_ids": [7, 8, 9], "attention_mask": [1, 1, 1]},
    ]
    return DummyIterableDataset(data)

# Test the length of the CustomDataset
def test_custom_dataset_length(dummy_dataset):
    custom_dataset = CustomDataset(dummy_dataset, length=3)
    assert len(custom_dataset) == 3

# Test the __getitem__ method
def test_custom_dataset_getitem(dummy_dataset):
    custom_dataset = CustomDataset(dummy_dataset, length=3)

    # Test accessing items
    assert custom_dataset[0] == {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}
    assert custom_dataset[1] == {"input_ids": [4, 5, 6], "attention_mask": [1, 1, 1]}
    assert custom_dataset[2] == {"input_ids": [7, 8, 9], "attention_mask": [1, 1, 1]}

    # Test caching (index_to_item)
    assert 0 in custom_dataset.index_to_item
    assert 1 in custom_dataset.index_to_item
    assert 2 in custom_dataset.index_to_item

# Test out-of-range index
def test_custom_dataset_out_of_range(dummy_dataset):
    custom_dataset = CustomDataset(dummy_dataset, length=3)

    with pytest.raises(IndexError, match="Index 3 is out of range."):
        _ = custom_dataset[3]

# Test edge case: Empty dataset
def test_custom_dataset_empty():
    class EmptyIterableDataset(Dataset):
        def __len__(self):
            return 0

        def __getitem__(self, index):
            raise IndexError("Empty dataset")

    empty_dataset = EmptyIterableDataset()
    custom_dataset = CustomDataset(empty_dataset, length=0)

    assert len(custom_dataset) == 0

    with pytest.raises(IndexError, match="Index 0 is out of range."):
        _ = custom_dataset[0]

# Test edge case: Length mismatch
def test_custom_dataset_length_mismatch(dummy_dataset):
    # Length provided is greater than the actual dataset length
    custom_dataset = CustomDataset(dummy_dataset, length=5)

    with pytest.raises(IndexError, match="Index 3 is out of range."):
        _ = custom_dataset[3]

# Test edge case: Negative index
def test_custom_dataset_negative_index(dummy_dataset):
    custom_dataset = CustomDataset(dummy_dataset, length=3)

    with pytest.raises(IndexError, match="Index -1 is out of range."):
        _ = custom_dataset[-1]