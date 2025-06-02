import torch
import torch.nn as nn
import torch.optim as optim
import gc
import os
import json
from utils import preTrainDataset
from utils import save_model, load_model, draw
from torch.utils.data import DataLoader
from CNN import CNN, PolicyNet, ValueNet, pretrain, train_PolicyNet, train_ValueNet
from readGameRecord import readGameRecord
from AbaloneEnv import AbaloneEnv
from play import play
from tqdm import tqdm

workDir = os.getcwd()

# pretrain Policy Network using record generate by Minmax
def behavior_cloning():
    
    n = 5
    train_data, train_label = readGameRecord(n)
    train_dataset = preTrainDataset(train_data, train_label)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policyNetwork = CNN(n).to(device)
    criterion = nn.CrossEntropyLoss()

    base_params = [param for _, param in policyNetwork.named_parameters()]
    optimizer = optim.Adam(base_params, lr=1e-4)

    _, losses, epoch = pretrain(policyNetwork, train_loader, criterion, optimizer, device)

    draw(int(epoch), losses)

    save_model(policyNetwork, './python_main_Env/model/policyNetwork_pretrain.pth')


def RL_policyNetwork():

    n = 5
    epoch = 1000
    losses = []

    policy = load_model('./python_main_Env/model/policyNetwork_pretrain.pth', n)
    opponent = load_model('./python_main_Env/model/policyNetwork_pretrain.pth', n)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_params = [param for _, param in policy.named_parameters()]
    optimizer = optim.Adam(base_params, lr=5*1e-4)
    
    min_loss = 1e10
    for i in tqdm(range(epoch)):
        env = AbaloneEnv()
        
        if i != 0: 
            policy.load_state_dict(torch.load(f'./python_main_Env/model/policy_{i-1}.pth'))

        loss = train_PolicyNet(env, policy, opponent, optimizer, device)
        losses.append(loss.detach().cpu().item())


        with open (workDir + "/python_main_Env/losses/policy_loss.json", 'r', encoding="utf-8") as file:
            data: list = json.load(file)
        data.append(loss.detach().cpu().item())
        with open (workDir + "/python_main_Env/losses/policy_loss.json", 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        save_model(policy, f'./python_main_Env/model/policy_{i}.pth')

        if loss < min_loss:
            save_model(policy, f'./python_main_Env/bestModel.pth')
            min_loss = loss

    

    draw(epoch, losses)

def RL_valueNetwork():

    n = 5
    epoch = 1000
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    value_net = ValueNet(n).to(device)
    optimizer = torch.optim.Adam(value_net.parameters(), lr=1e-8)
    policy = load_model('./python_main_Env/model/policy_500.pth', n)
    opponent = load_model('./python_main_Env/model/policy_500.pth', n)
    losses = []

    min_loss = 1e10
    for i in tqdm(range(epoch)):
        policy_reward, _, states, T = play(policy, opponent)
        if policy_reward == 0:
            policy_reward = -1
        loss = train_ValueNet(value_net, states, T, n, policy_reward, optimizer, device)
        losses.append(loss)

        save_model(value_net, f'./python_main_Env/model/valueNet/value_{i}.pth')

        with open (workDir + "/python_main_Env/losses/value_loss.json", 'r', encoding="utf-8") as file:
            data: list= json.load(file)
        data.append(loss.detach().cpu().item())    
        with open (workDir + "/python_main_Env/losses/value_loss.json", 'w', encoding="utf-8") as file:
            
            json.dump(data, file, ensure_ascii=False, indent=4)

        if loss < min_loss:
            save_model(value_net, f'./python_main_Env/bestValueModel2.pth')
            min_loss = loss

        torch.cuda.empty_cache()
        gc.collect()

    draw(epoch, losses)


if __name__ == '__main__':
    #behavior_cloning()
    RL_policyNetwork()
    #RL_valueNetwork()