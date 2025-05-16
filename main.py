import torch
import torch.nn as nn
import torch.optim as optim
from utils import TrainDataset, save_model, load_model
from torch.utils.data import DataLoader
from CNN import CNN, train
from readGameRecord import readGameRecord

# pretrain Policy Network using record generate by Minmax
def behavior_cloning():
   
    train_data, train_label = readGameRecord()
    train_dataset = TrainDataset(train_data, train_label)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policyNetwork = CNN().to(device)
    criterion = nn.CrossEntropyLoss()

    base_params = [param for _, param in policyNetwork.named_parameters()]
    optimizer = optim.Adam(base_params, lr=1.5*1e-4)

    train(policyNetwork, train_loader, criterion, optimizer, device)

    save_model(policyNetwork, './model/policyNetwork_pretrain.pth')

# self playing (not done yet)
def RL_policyNetwork():
    player = load_model('./model/policyNetwork_pretrain.pth')
    opponent = player
    player.train()
    opponent.eval()

if __name__ == '__main__':
    behavior_cloning()
    RL_policyNetwork()