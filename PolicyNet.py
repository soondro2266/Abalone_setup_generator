import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from AbaloneEnv import AbaloneEnv
from CNN import CNN_

n = 5
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

policy = CNN_(n).to(device)
optimizer = optim.Adam(policy.parameters(), lr=1e-4)

def train_one_episode(env: AbaloneEnv, policy, optimizer):
    log_probs, rewards = [], []
    state = env.get_state_tensor()
    print(type(state))
    done = False

    # 蒐集軌跡
    while not done:
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)  # (1,4,9,9)
        probs = policy(s).squeeze(0)
        all_possible_action = env.get_all_actions()  
        legal_probs = probs[all_possible_action]        # shape [n_legal]

        legal_probs = legal_probs / legal_probs.sum()

        dist = torch.distributions.Categorical(legal_probs)
        a = dist.sample()
        idx_in_legal = a.item()   
        action = all_possible_action[idx_in_legal]  
        log_probs.append(dist.log_prob(a))
        state, r, done = env.step(action)
        rewards.append(r)

    # 計算折扣回報 G_t（也可以改成不折扣）
        
    returns = torch.tensor(np.full(len(rewards), rewards[-1], dtype=torch.float32), device=device)

    # 損失：－Σ log π(a|s) * G_t
    loss = 0
    for log_p, Gt in zip(log_probs, returns):
        loss = loss - log_p * Gt
    loss = loss / len(log_probs)  # optional：平均化

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return sum(rewards)

"""
def play_one_episode(env: AbaloneEnv, policy, greedy=False):
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
"""
