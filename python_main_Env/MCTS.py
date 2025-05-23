import os
import torch
import numpy as np
from CNN import PolicyNet, ValueNet
from AbaloneEnv import AbaloneEnv
from utils import load_model

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

print(model_path)

class node_info:
    def __init__(self, action_count):
        self.action_count = action_count
        self.q = np.zeros((action_count, ), dtype = np.float32)
        self.n = np.zeros((action_count, ), dtype = np.int32)

class MCTS:
    def __init__(self, n = 5, eta = 1e-4, value_path = "best_model.pth", policy_path = "best_model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.value_network = ValueNet(n).to(self.device)
        self.policy_network = PolicyNet(n).to(self.device)
        self.value_network.load_state_dict(torch.load(model_path+"\\valueNet\\"+ value_path))
        self.policy_network.load_state_dict(torch.load(model_path+"\\policyNet\\"+ policy_path))
        self.value_network.eval()
        self.policy_network.eval()
        

        self.place_count = 3 * n * (n - 1) + 1
        self.edge = n
        self.action_count = self.place_count * 42

        self.searching_data:dict[str, node_info] = {}

        self.game = AbaloneEnv(n = n)

        self.eta = eta



    def selection(self)->int:
        all_possible_action = self.game.get_all_actions()
        current_state = self.game.load_state_string()

        current_info = self.searching_data.setdefault(current_state,node_info(self.action_count))

        policy_net_probility = self.policy_network(self.game.get_state_tensor())

        scores = []
        for action in all_possible_action:
            scores.append(current_info.q[action] + \
                          self.eta * policy_net_probility[action] / (1 + current_info.n[action]))
        
        seleted_action = all_possible_action[np.argmax(scores)]
        current_info.n[seleted_action] += 1

        return seleted_action
    
    def expansion(self, action:int):

        self.game.step(action) #state become state'

        all_possible_action_prime = self.game.get_all_actions()
        policy_net_probility = self.policy_network(self.game.get_state_tensor())

        all_possible_probility = policy_net_probility[all_possible_action_prime]        
        all_possible_probility = all_possible_probility / all_possible_probility.sum()

        dist = torch.distributions.Categorical(all_possible_probility)
        a = dist.sample()  
        action_prime = all_possible_action_prime[a.item()]

        self.game.step(action_prime) #state' become state t+1 

    

         
    
    
            




