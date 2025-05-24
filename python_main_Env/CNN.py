import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch.nn as nn

from AbaloneEnv import AbaloneEnv
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

class PolicyNet(nn.Module):
    def __init__(self, n):
        super(PolicyNet, self).__init__()
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
        x = F.softmax(x, dim=-1)
        return x
    

class ValueNet(nn.Module):
    def __init__(self, n):
        """
        n: Abalone 棋盤半徑參數，原始大小為 (2*n-1)*(2*n-1)
        輸入通道數同樣是 4(state tensor shape: (4, 2n-1, 2n-1))。
        """
        super(ValueNet, self).__init__()
        self.n = n

        # 1) shared 卷積特徵抽取層（完全照搬 Policy 的 convLayer）
        self.convLayer = nn.Sequential(
            nn.Conv2d(in_channels=4, out_channels=16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )

        # 2) 全連接層：先展平，再映射到隱藏維度，最後輸出一個標量
        hidden_dim = 16 * (2*n-1) * (2*n-1)
        feat_dim   = 64 * (2*n-1) * (2*n-1)
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(feat_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(hidden_dim, 1),   # 輸出一個標量 v(s)
            nn.Tanh(),                   # 壓縮到 [-1,1]
        )

    def forward(self, x):
        """
        x: FloatTensor of shape (batch_size, 4, 2n-1, 2n-1)
        return: FloatTensor of shape (batch_size,)  (scalar value for each state)
        """
        h = self.convLayer(x)
        v = self.fc(h).squeeze(-1)
        return v

def pretrain(model: CNN, train_loader: DataLoader, criterion, optimizer, device):
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

def train_PolicyNet(env: AbaloneEnv, policy: PolicyNet, opponent: PolicyNet, optimizer, device: torch.device)-> torch.Tensor:
    policy.train()
    opponent.eval()
    log_probs = []
    reward = 0
    policy_reward = 0
    state = env.get_state_tensor()
    done = False

    player = [None, policy, opponent]
    turn = 1

    while not done:
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)  # (1,4,9,9)
        probs = player[turn](s).squeeze(0)

        all_possible_action = env.get_all_actions()  
        
        stepSuccess = False
        while not stepSuccess:
            legal_probs = probs[all_possible_action]        
            if legal_probs.sum() == 0:
                legal_probs = torch.ones_like(legal_probs) / len(legal_probs)
            else:
                legal_probs = legal_probs / legal_probs.sum()
            legal_probs = legal_probs / legal_probs.sum()
            dist = torch.distributions.Categorical(legal_probs)
            a = dist.sample()
            idx_in_legal = a.item()   
            action = all_possible_action[idx_in_legal]
            state, reward, done, stepSuccess = env.step(action)
            if not stepSuccess:
                all_possible_action.remove(action)

        if player[turn] == policy:  
            log_probs.append(dist.log_prob(a))

        turn *= -1
    
    if reward == 1:
        policy_reward = 1
    else:
        policy_reward = -1
        
    returns = torch.full((len(log_probs),), policy_reward,dtype=torch.float32,device=device)

    loss = 0
    for log_p, Gt in zip(log_probs, returns):
        loss = loss - log_p * Gt
    loss = loss / len(log_probs) 

    loss = loss.to(device)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss

def train_ValueNet(value_net, states, T: int, n: int, policy_reward: int, optimizer, device)-> torch.Tensor:


    # 將 T 個 state 疊成一個 batch
    S = torch.stack(states, dim=0).to(device)          # shape: (T,4,2n-1,2n-1)
    U = torch.full((T,), policy_reward, device=device, dtype=torch.float32)  # 即 u_t

    V_hat = value_net(S)                               # shape: (T,)
    loss  = 0.5 * F.mse_loss(V_hat, U, reduction='sum') # L = Σ ½ (v - u)^2

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss