import torch
from AbaloneEnv import AbaloneEnv
from utils import load_model

@torch.no_grad()
def play():

    env = AbaloneEnv()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy = load_model("/home/wlog/Desktop/Abalone_setup_generator/model/policy_999.pth", 5)
    policy.eval()

    terminate = False

    while not terminate:
        state = env.get_state_tensor()
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        pi = policy(s).squeeze(0)
        possible_action = env.get_all_actions()
        best_action = possible_action[0]

        for action in possible_action:
            if pi[action] > pi[best_action]:
                best_action = action

        _, _, terminate = env.step(best_action)
        env.show_current_board()

play()

