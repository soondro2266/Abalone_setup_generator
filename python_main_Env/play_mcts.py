import os
import copy
import json
import torch
import numpy as np
from tqdm import tqdm
from utils import load_model
from MCTS import MCTS
from CNN import PolicyNet
from AbaloneEnv import AbaloneEnv

best_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_model")

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

@torch.no_grad()
def play_mcts(mcts_p: MCTS, policy_op: PolicyNet, mcts_record: str, num_of_simu: int):

    env = AbaloneEnv()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    turn = 1

    done = False
    while not done:
        
        env.show_current_board()
        if turn:
            env_ = copy.deepcopy(env)

            for _ in range(num_of_simu):
                mcts_p.one_simulation(env_)

            with open(mcts_record, 'r', encoding="utf-8") as f:
                data: dict[str, dict[int, list]] = json.load(f)

            state_t_str = env.load_state_string()
            score = []
            for info in data[state_t_str].values():
                q = 0 if info[1] == 0 else info[2] / info[1]
                score.append(q + mcts_p.eta * info[0] / (1 + info[1]))
            selected_action_t = list(data[state_t_str].keys())[np.argmax(score)]
            
            _, _, done, _ = env.step(int(selected_action_t))

            if done:
                print("mcts win")
            
        else:
            s = torch.tensor(env.get_state_tensor(), dtype=torch.float32).unsqueeze(0).to(device)
            probs = policy_op(s).squeeze(0)
            all_possible_action = env.get_all_actions()  

            stepSuccess = False
            while not stepSuccess:
                legal_probs = probs[all_possible_action]        
                if legal_probs.sum() == 0:
                    legal_probs = torch.ones_like(legal_probs) / len(legal_probs)
                else:
                    legal_probs = legal_probs / legal_probs.sum()

                dist = torch.distributions.Categorical(legal_probs)
                a = dist.sample()
                idx_in_legal = a.item()   
                best_action = all_possible_action[idx_in_legal]
                all_possible_action.remove(best_action)

                _, _, done, stepSuccess = env.step(best_action)
            
            if done:
                print("opponent win")

        
        turn = not turn

if __name__ == '__main__':
    
    policy_path_p = "bestPolicyModel_.pth"
    value_path_p = "bestValueModel.pth"
    policy_path_op = model_path + "/policyNetwork_pretrain.pth"
    mcts_p = MCTS(value_path=value_path_p, policy_path=policy_path_p)
    policy_op = load_model(policy_path_op)
    policy_op.eval()
    mcts_record = best_model_path + "/mcts.json"
    num_of_simu = 50

    epoch = 1
    for _ in tqdm(range(epoch)):
        play_mcts(mcts_p, policy_op, mcts_record, num_of_simu)