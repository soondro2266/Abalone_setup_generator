import torch
import torch.nn as nn
import torch.optim as optim
from utils import preTrainDataset
from utils import save_model, load_model, draw
from torch.utils.data import DataLoader
from CNN import CNN, pretrain, CNN_, train
from readGameRecord import readGameRecord
from AbaloneEnv import AbaloneEnv
from tqdm import tqdm

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

    pretrain(policyNetwork, train_loader, criterion, optimizer, device)

    save_model(policyNetwork, './model/policyNetwork_pretrain.pth')


def RL_policyNetwork():

    n = 5
    epoch = 100
    losses = []

    policy = load_model('./model/policy_99.pth', n)
    opponent = policy
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_params = [param for _, param in policy.named_parameters()]
    optimizer = optim.Adam(base_params, lr=2*1e-4)
    

    for i in tqdm(range(epoch)):
        env = AbaloneEnv()
        
        if i != 0: 
            policy.load_state_dict(torch.load(f'./model/policy_{i-1}.pth'))

        loss = train(env, policy, opponent, optimizer, device)
        losses.append(loss.detach().item())

        save_model(policy, f'./model/policy_{i}.pth')

    save_model(policy, f'./bestModel.pth')

    draw(epoch, losses)



if __name__ == '__main__':
    #behavior_cloning()
    RL_policyNetwork()