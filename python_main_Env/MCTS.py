import os
import json
import torch
import numpy as np
from CNN import PolicyNet, ValueNet
from AbaloneEnv import AbaloneEnv
from utils import load_model

best_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_model")

print(best_model_path)


class MCTS:
    def __init__(self, n: int = 5, eta = 1e-4, value_path = "best_model.pth", policy_path = "best_model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.value_network = ValueNet(n).to(self.device)
        self.policy_network = PolicyNet(n).to(self.device)
        self.value_network.load_state_dict(torch.load(best_model_path + "/" + value_path))
        self.policy_network.load_state_dict(torch.load(best_model_path + "/" + policy_path))
        self.mcts_record_path = best_model_path + "/mcts.json"
        self.value_network.eval()
        self.policy_network.eval()
        
        self.edge = n

        self.eta = eta

    @torch.no_grad()
    def one_simulation(self, env:AbaloneEnv)->None:
        with open(self.mcts_record_path, 'r', encoding='utf-8') as f:
            data: dict[str, dict[int, list]] = json.load(f)
        
        state_t_str = env.load_state_string()
        if state_t_str not in data:
            s = torch.tensor(env.get_state_tensor(), dtype=torch.float32).unsqueeze(0).to(self.device)
            policy_net_probility = self.policy_network(s).squeeze(0)
            all_possible_action_t = env.get_all_actions()
            data[state_t_str] = {}
            for action_t in all_possible_action_t:
                data[state_t_str][action_t] = [0, 0, 0] #pi, N, Vsum
                data[state_t_str][action_t][0] = policy_net_probility[action_t].detach().cpu().tolist()
        
        scores = []
        for info in data[state_t_str].values():
            q = 0 if info[1] == 0 else info[2]/info[1]
            scores.append(q + \
                          self.eta * info[0] / (1 + info[1]))
        
        seleted_action_t = list(data[state_t_str].keys())[np.argmax(scores)]

        #selection finished

        env.step(int(seleted_action_t))

        #expansion start

        all_possible_action_prime = env.get_all_actions()
        s = torch.tensor(env.get_state_tensor(), dtype=torch.float32).unsqueeze(0).to(self.device)
        policy_net_probility = self.policy_network(s).squeeze(0)

        all_possible_probility = policy_net_probility[all_possible_action_prime]        
        all_possible_probility = all_possible_probility / all_possible_probility.sum()

        dist = torch.distributions.Categorical(all_possible_probility)
        a = dist.sample()  
        action_prime = all_possible_action_prime[a.item()]

        env.step(action_prime) #state' become state t+1

        #evaluation on state t+1

        """
        s = torch.tensor(env.get_state_tensor(), dtype=torch.float32).unsqueeze(0).to(self.device)
        valueNet_score = self.value_network(s).squeeze(0)
        """
        

        done = env.finished
        reward = 0
        while not done:
            all_possible_action = env.get_all_actions()
            s = torch.tensor(env.get_state_tensor(), dtype=torch.float32).unsqueeze(0).to(self.device)
            policy_net_probility = self.policy_network(s).squeeze(0)

            all_possible_probility = policy_net_probility[all_possible_action]        
            all_possible_probility = all_possible_probility / all_possible_probility.sum()

            dist = torch.distributions.Categorical(all_possible_probility)
            a = dist.sample()  
            action = all_possible_action[a.item()]

            stepSuccess = False
            while not stepSuccess:
                all_possible_probility = policy_net_probility[all_possible_action]        
                all_possible_probility = all_possible_probility / all_possible_probility.sum()

                dist = torch.distributions.Categorical(all_possible_probility)
                a = dist.sample()  
                action = all_possible_action[a.item()]
                all_possible_action.remove(action)
                _, reward, done, stepSuccess = env.step(action)
        
        v = reward

        data[state_t_str][seleted_action_t][1] += 1
        data[state_t_str][seleted_action_t][2] += v


        with open(self.mcts_record_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False 允許中文不被轉為 \u 編碼
            # indent=4 自動排版成易讀的格式
            json.dump(data, f, ensure_ascii=False, indent=4)

        return