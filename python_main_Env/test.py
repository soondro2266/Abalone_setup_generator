import torch
import os
from utils import load_model
from AbaloneEnv import AbaloneEnv

currentPath = os.getcwd()
env = AbaloneEnv()
device = torch.device("cuda")
value = load_model(currentPath + "/python_main_Env/best_model/bestValueModel.pth")
value.eval()

state = env.get_state_tensor()
s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)

pred = value(s)

print(pred)