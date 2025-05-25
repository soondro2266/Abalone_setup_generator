import os
import json
import torch
import numpy as np
from CNN import PolicyNet, ValueNet
from AbaloneEnv import AbaloneEnv
from utils import load_model

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

print(model_path)


class MCTS:
    def __init__(self, n = 5, eta = 1e-4, value_path = "best_model.pth", policy_path = "best_model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.value_network = ValueNet(n).to(self.device)
        self.policy_network = PolicyNet(n).to(self.device)
        self.value_network.load_state_dict(torch.load(model_path+"/valueNet/"+ value_path))
        self.policy_network.load_state_dict(torch.load(model_path+"/policyNet/"+ policy_path))
        self.mcts_record_path = model_path + "/mcts.json"
        self.value_network.eval()
        self.policy_network.eval()
        
        self.edge = n

        self.eta = eta

    def one_simulation(self, env:AbaloneEnv)->None:
        with open(self.mcts_record_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        state_t_str = env.load_state_string()
        if state_t_str not in data:
            policy_net_probility = self.policy_network(env.get_state_tensor())
            all_possible_action_t = env.get_all_actions()
            data[state_t_str] = {}
            for action_t in all_possible_action_t:
                data[state_t_str][action_t] = [0, 0, 0] #pi, N, Vsum
                data[state_t_str][action_t][0] = policy_net_probility[action]
        
        scores = []
        for info in data[state_t_str].values():
            q = 0 if info[1] == 0 else info[2]/info[1]
            scores.append(q + \
                          self.eta * info[0] / (1 + info[1]))
        
        seleted_action_t = data[state_t_str].keys()[np.argmax(scores)]

        #selection finished

        env.step(seleted_action_t)

        #expansion start

        all_possible_action_prime = env.get_all_actions()
        policy_net_probility = self.policy_network(env.get_state_tensor())

        all_possible_probility = policy_net_probility[all_possible_action_prime]        
        all_possible_probility = all_possible_probility / all_possible_probility.sum()

        dist = torch.distributions.Categorical(all_possible_probility)
        a = dist.sample()  
        action_prime = all_possible_action_prime[a.item()]

        env.step(action_prime) #state' become state t+1

        #evaluation on state t+1

        state = env.get_state_tensor()
        valueNet_score = self.value_network(state)


        done = env.finished
        reward = 0
        while not done:
            all_possible_action = env.get_all_actions()
            policy_net_probility = self.policy_network(state)

            all_possible_probility = policy_net_probility[all_possible_action]        
            all_possible_probility = all_possible_probility / all_possible_probility.sum()

            dist = torch.distributions.Categorical(all_possible_probility)
            a = dist.sample()  
            action = all_possible_action[a.item()]

            state, reward, done = env.step(action)
        
        v = 0.5 * (valueNet_score + reward)

        data[state_t_str][seleted_action_t][1] += 1
        data[state_t_str][seleted_action_t][2] += v

        with open(self.mcts_record_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False 允許中文不被轉為 \u 編碼
            # indent=4 自動排版成易讀的格式
            json.dump(data, f, ensure_ascii=False, indent=4)

        return