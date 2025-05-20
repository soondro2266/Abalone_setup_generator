import torch
import torch.nn as nn
import torch.optim as optim
from utils import TrainDataset, save_model, load_model
from torch.utils.data import DataLoader
from CNN import CNN, train
from readGameRecord import readGameRecord
from PolicyNet import train_one_episode
from AbaloneEnv import AbaloneEnv
from tqdm import tqdm

# pretrain Policy Network using record generate by Minmax
def behavior_cloning():
    
    n = 5
    train_data, train_label = readGameRecord(n)
    train_dataset = TrainDataset(train_data, train_label)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policyNetwork = CNN(n).to(device)
    criterion = nn.CrossEntropyLoss()

    base_params = [param for _, param in policyNetwork.named_parameters()]
    optimizer = optim.Adam(base_params, lr=1e-4)

    train(policyNetwork, train_loader, criterion, optimizer, device)

    save_model(policyNetwork, './model/policyNetwork_pretrain.pth')


def RL_policyNetwork():

    n = 5
    policy = load_model('./model/policyNetwork_pretrain.pth', n)

    epoch = 1000
    policy.train()

    for i in tqdm(range(epoch)):
        env = AbaloneEnv()
        base_params = [param for _, param in policy.named_parameters()]
        optimizer = optim.Adam(base_params, lr=1e-4)
        if i != 0: 
            policy = load_model(f'./model/policy_{i-1}.pth', n)

        train_one_episode(env, policy, optimizer)

        save_model(policy, f'./model/policy_{i}.pth')



if __name__ == '__main__':
    #behavior_cloning()
    RL_policyNetwork()