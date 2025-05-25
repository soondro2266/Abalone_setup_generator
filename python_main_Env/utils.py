import torch
from torch.utils.data import Dataset
from CNN import CNN, PolicyNet
import matplotlib.pyplot as plt

class preTrainDataset(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        data = torch.tensor(self.data[idx], dtype=torch.float32)
        label = self.label[idx]
        return data, label
    

def save_model(model: torch.nn, path: str):
    torch.save(model.state_dict(), path)



def load_model(path: str, n: int):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PolicyNet(n).to(device)
    model.load_state_dict(torch.load(path))
    return model

def draw(epoch: int, losses: list):
    x = [i for i in range(epoch)]
    y = losses
    plt.plot(x, y, color='blue', linewidth=2, marker='.')    
    plt.xlabel("epoch")
    plt.ylabel("loss")                
    plt.savefig('epoch-loss.png')
    plt.show()   