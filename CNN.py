import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch.nn as nn
from tqdm import tqdm

class CNN(nn.Module):
    def __init__(self, n):
        super(CNN, self).__init__()
        self.n = n
        # No pooling due to original size is too small (9*9)
        self.convLayer = nn.Sequential(
            nn.Conv2d(in_channels=4, out_channels=16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.fullConnect = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64*(2*n-1)*(2*n-1), 16*(2*n-1)*(2*n-1)),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(16*(2*n-1)*(2*n-1), 42*(3*n*n-3*n+1)),
        )
    def forward(self, x):
        x = self.convLayer(x)
        x = self.fullConnect(x)
        return x

class CNN_(nn.Module):
    def __init__(self, n):
        super(CNN_, self).__init__()
        self.n = n
        # No pooling due to original size is too small (9*9)
        self.convLayer = nn.Sequential(
            nn.Conv2d(in_channels=4, out_channels=16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.fullConnect = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64*(2*n-1)*(2*n-1), 16*(2*n-1)*(2*n-1)),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(16*(2*n-1)*(2*n-1), 42*(3*n*n-3*n+1)),
        )
    def forward(self, x):
        x = self.convLayer(x)
        x = self.fullConnect(x)
        x = F.softmax(x)
        return x

def train(model: CNN, train_loader: DataLoader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    num_batch = 0.0
    for data, label in tqdm(train_loader):
        data = data.to(device)
        label = label.to(device)
        optimizer.zero_grad()
        pi_hat = model(data)
        train_loss = criterion(pi_hat, label)
        train_loss.backward()
        optimizer.step()
        total_loss += train_loss.detach().item()
        num_batch += 1.0
    avg_loss = total_loss/num_batch
    return avg_loss