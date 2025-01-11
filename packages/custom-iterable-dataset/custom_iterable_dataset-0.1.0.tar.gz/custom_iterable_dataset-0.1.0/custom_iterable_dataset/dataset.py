from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self,dataset, length):
        self.iterable_dataset = dataset
        self.length = length
        self.index_to_item = {}
        
    
    def _create_generator(self,num):
        counter = 0
        for sample in self.iterable_dataset:
            yield sample
            if counter == num : break
            counter += 1

    def __len__(self):
        return self.length
    
    def __getitem__(self,index):
        if index in self.index_to_item:
            return self.index_to_item[index]
        else:
            subset = self._create_generator(num=index)
            for i,item in enumerate(subset):
                if i == index:
                    self.index_to_item[index] = item
                    return item
            raise IndexError(f"Index {index} is out of range.")
