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
    def forward(self, x)-> torch.Tensor:
        x = self.convLayer(x)
        x = self.fullConnect(x)
        x = F.softmax(x, dim=-1)
        return x
    

class ValueNet(nn.Module):
    def __init__(self, n: int):
        """
        n: Abalone 棋盤半徑參數，原始大小為 (2*n-1)*(2*n-1)
        輸入通道數同樣是 4(state tensor shape: (4, 2n-1, 2n-1))。
        """
        super(ValueNet, self).__init__()
        self.n: int = n

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
            nn.Dropout(0.3),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, 1),   # 輸出一個標量 v(s)          
            nn.Tanh()         
        )

    def forward(self, x)-> torch.Tensor:
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
    losses = []
    for _ in range(100):
        for data, label in tqdm(train_loader):
            data = data.to(device)
            label = label.to(device)
            optimizer.zero_grad()
            pi_hat = model(data)
            train_loss = criterion(pi_hat, label)
            train_loss.backward()
            optimizer.step()
            total_loss += train_loss.detach().item()
            losses.append(train_loss.detach().cpu().item())
            num_batch += 1.0
    avg_loss = total_loss/num_batch
    return avg_loss, losses, num_batch

def train_PolicyNet(env: AbaloneEnv, 
                    policy: PolicyNet, 
                    opponent: PolicyNet, 
                    optimizer, 
                    device: torch.device, 
                    penalty_coef: float = 0.1)-> torch.Tensor:
    policy.train()
    opponent.eval()
    log_probs = []
    reward = 0
    policy_reward = 0
    penalty_sum  = 0.0
    state = env.get_state_tensor()
    done = False

    player = [None, policy, opponent]
    turn = 1

    while not done:
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)  # (1,4,9,9)
        if player[turn] is policy:
            probs = policy(s).squeeze(0)
        else:
            with torch.no_grad():
                probs = opponent(s).squeeze(0)

        legal_action_index = env.get_all_actions()
        illegal_mask = torch.ones_like(probs) #1 is illegal 0 is legal
        illegal_mask[legal_action_index] = 0
        illegal_prob = (probs * illegal_mask).sum()
        
        stepSuccess = False
        while not stepSuccess:
            legal_probs = probs[legal_action_index]
            if legal_probs.sum() == 0:
                legal_probs = legal_probs + 1e-8
            legal_probs = legal_probs / legal_probs.sum()
            dist = torch.distributions.Categorical(legal_probs)
            a   = dist.sample()
            idx_in_legal = a.item()
            action = legal_action_index[idx_in_legal]
            state, reward, done, stepSuccess = env.step(action)
            if not stepSuccess:
                legal_action_index.remove(action)

        if player[turn] == policy:  
            log_probs.append(dist.log_prob(a))
            penalty_sum += illegal_prob


        del dist, a, legal_probs, probs, s
        turn *= -1
    
    if reward == 1:
        policy_reward = 1
    else:
        policy_reward = -1
        
    returns = torch.full((len(log_probs),), policy_reward,dtype=torch.float32,device=device)

    pg_loss = 0
    for log_p, Gt in zip(log_probs, returns):
        pg_loss = pg_loss - log_p * Gt
    pg_loss = pg_loss / len(log_probs) 

    penalty_loss = penalty_coef * (penalty_sum / len(log_probs))

    loss = pg_loss + penalty_loss

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    torch.cuda.empty_cache()

    return loss

def train_ValueNet(value_net, states, T, n, policy_reward, optimizer, device):

    gamma = 0.99
    S = torch.stack(states, dim=0).to(device)
    U = torch.tensor([policy_reward * (gamma ** (T - 1 - t)) for t in range(T)], device=device)

    V_hat = value_net(S)
    loss  = F.mse_loss(V_hat, U, reduction='mean')

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    loss_ = loss.detach().cpu().item()

    del loss, V_hat, S, U

    return loss_
