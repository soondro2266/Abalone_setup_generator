import torch
from torch.utils.data import Dataset
from torchvision import transforms
from CNN import CNN

class TrainDataset(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        data = transforms.ToTensor(self.data[idx])
        label = self.label[idx]
        return data, label
    

def save_model(model: CNN, path: str):
    torch.save(model.state_dict(), path)


def load_model(path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CNN().to(device)
    model.load_state_dict(torch.load(path))
    return model