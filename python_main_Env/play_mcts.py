import os
import copy
import json
import torch
import numpy as np
from tqdm import tqdm
from MCTS import MCTS
from AbaloneEnv import AbaloneEnv

best_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_model")

@torch.no_grad()
def play_mcts(mcts_p: MCTS, mcts_op: MCTS, mcts_record: str, num_of_simu: int):

    env = AbaloneEnv()
    mcts_player: dict[int, MCTS] = [None, mcts_p, mcts_op]
    turn = 1

    done = False
    while not done:
        env_ = copy.deepcopy(env)

        for _ in range(num_of_simu):
            mcts_player[turn].one_simulation(env_)

        with open(mcts_record, 'r', encoding="utf-8") as f:
            data: dict[str, dict[int, list]] = json.load(f)

        state_t_str = env.load_state_string()
        score = []
        for info in data[state_t_str].values():
            q = 0 if info[1] == 0 else info[2] / info[1]
            score.append(q + mcts_player[turn].eta * info[0] / (1 + info[1]))
        selected_action_t = data[state_t_str].keys()[np.argmax(score)]
        
        _, _, done, _ = env.step(selected_action_t)
        turn *= -1

if __name__ == '__main__':
    policy_path_p = "bestPolicyModel.pth"
    value_path_p = "bestValueModel.pth"
    policy_path_op = "bestPolicyModel.pth"
    value_path_op = "bestValueModel.pth"
    mcts_p = MCTS(value_path=value_path_p, policy_path=policy_path_p)
    mcts_op = MCTS(value_path=value_path_op, policy_path=policy_path_op)
    mcts_record = model_path = "/mcts.json"
    num_of_simu = 300

    epoch = 100
    for _ in tqdm(range(epoch)):
        play_mcts(mcts_p, mcts_op, mcts_record, num_of_simu)