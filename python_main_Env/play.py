import torch
from AbaloneEnv import AbaloneEnv
from tqdm import tqdm
from CNN import PolicyNet
from utils import load_model


@torch.no_grad()
def play(policy_, opponent_):

    env = AbaloneEnv()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy = policy_
    opponent = opponent_
    policy.eval()
    opponent.eval()
    policy_win = 0
    opponent_win = 0
    states = []
    T = 0

    terminate = False

    player = [None, policy, opponent]
    turn = 1
    while not terminate:
        state = env.get_state_tensor()
        if turn == 1:
            states.append(torch.tensor(state))
            T += 1
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)

        probs = player[turn](s).squeeze(0)

        all_possible_action = env.get_all_actions()  
        

        turn *= -1

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
            _, _, terminate, stepSuccess = env.step(best_action)
            all_possible_action.remove(best_action)
       
        if terminate:
            if player[turn] == policy:
                policy_win += 1
            if player[turn] == opponent:
                opponent_win += 1
        #env.show_current_board()
    
    states = tuple(states)
    return policy_win, opponent_win, states, T

def multi_play(policy_model_name: str, opponent_model_name: str, round_: int, n: int):
    policy = load_model(f"./python_main_Env/{policy_model_name}.pth", n)
    opponent = load_model(f"./python_main_Env/{opponent_model_name}.pth", n)
    round = round_
    policy_wins = 0
    opponent_wins = 0

    for _ in tqdm(range(round)):
        policy_win, opponent_win, _, _ = play(policy, opponent)
        policy_wins += policy_win
        opponent_wins += opponent_win
        
    print(f"policy win: {policy_wins}/{round}, using model: {policy_model_name}")
    print(f"opponent win: {opponent_wins}/{round}, using model: {opponent_model_name}")

if __name__ == '__main__':
    multi_play("bestPolicyModel", "bestPolicyModel", 50, 5)
