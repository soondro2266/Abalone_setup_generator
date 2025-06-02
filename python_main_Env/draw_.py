import os
import json
from utils import draw

workDir = os.getcwd() 

with open(workDir + "/python_main_Env/losses/policy_loss.json", "r", encoding="utf-8") as file:
    losses = json.load(file)

draw(len(losses), losses)