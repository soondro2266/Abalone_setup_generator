import torch
import torch.nn as nn
import torch.nn.functional as F

class ValueNet(nn.Module):
    def __init__(self, n):
        """
        n: Abalone 棋盤半徑參數，原始大小為 (2*n-1)×(2*n-1)
        輸入通道數同樣是 4（state tensor shape: (4, 2n-1, 2n-1)）。
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
    
value_net = ValueNet(n).to(device)
optimizer = torch.optim.Adam(value_net.parameters(), lr=1e-4)
criterion = nn.MSELoss()

# 將 T 個 state 疊成一個 batch
S = torch.stack(states, dim=0).to(device)          # shape: (T,4,2n-1,2n-1)
U = torch.full((T,), policy_reward, device=device, dtype=torch.float32)  # 即 u_t

V_hat = value_net(S)                               # shape: (T,)
loss  = 0.5 * F.mse_loss(V_hat, U, reduction='sum') # L = Σ ½ (v - u)^2

optimizer.zero_grad()
loss.backward()
optimizer.step()