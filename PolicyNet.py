import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class PolicyNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 假設 4 層 conv，保持 9×9 空間尺寸
        self.conv = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=3, padding=1),   # -> (32,9,9)
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # -> (64,9,9)
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1), # -> (128,9,9)
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),# -> (128,9,9)
            nn.ReLU(),
        )
        # 全連接層，輸出維度改為 2562
        self.fc = nn.Linear(128 * 9 * 9, 2562)

    def forward(self, x):
        """
        x: (B,4,9,9)  
        return: (B,2562) 經 softmax 後的動作機率分佈
        """
        B = x.size(0)
        h = self.conv(x)          # (B,128,9,9)
        h = h.view(B, -1)         # (B,128*9*9)
        logits = self.fc(h)       # (B,2562)
        probs = F.softmax(logits, dim=1)
        return probs

policy = PolicyNet().to(device)
optimizer = optim.Adam(policy.parameters(), lr=1e-4)

def train_one_episode(env, policy, optimizer, gamma=1.0):
    log_probs, rewards = [], []
    state = env.reset()
    done = False

    # 蒐集軌跡
    while not done:
        s = torch.from_numpy(state).float().unsqueeze(0).to(device)  # (1,4,9,9)
        probs = policy(s)                                           # (1,2562)
        dist = torch.distributions.Categorical(probs)
        a = dist.sample()                                           # 樣本動作
        log_probs.append(dist.log_prob(a))
        state, r, done, _ = env.step(a.item())
        rewards.append(r)

    # 計算折扣回報 G_t（也可以改成不折扣）
    G = 0
    returns = []
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)
    returns = torch.tensor(returns, device=device)

    # 損失：－Σ log π(a|s) * G_t
    loss = 0
    for log_p, Gt in zip(log_probs, returns):
        loss = loss - log_p * Gt
    loss = loss / len(log_probs)  # optional：平均化

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return sum(rewards)

def play_one_episode(env, policy, greedy=False):
    state = env.reset()
    done = False
    total_r = 0

    while not done:
        s = torch.from_numpy(state).float().unsqueeze(0).to(device)
        probs = policy(s)  # (1,2562)
        if greedy:
            a = torch.argmax(probs, dim=1).item()
        else:
            a = torch.distributions.Categorical(probs).sample().item()
        state, r, done, _ = env.step(a)
        total_r += r

    return total_r