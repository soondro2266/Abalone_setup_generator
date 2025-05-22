import torch
from AbaloneEnv import AbaloneEnv
from tqdm import tqdm
from CNN import CNN_
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

    terminate = False

    player = [None, policy, opponent]
    turn = 1
    while not terminate:
        state = env.get_state_tensor()
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)

        probs = player[turn](s).squeeze(0)

        all_possible_action = env.get_all_actions()  
        legal_probs = probs[all_possible_action]        
        legal_probs = legal_probs / legal_probs.sum()

        dist = torch.distributions.Categorical(legal_probs)
        a = dist.sample()
        idx_in_legal = a.item()   
        best_action = all_possible_action[idx_in_legal]

        """
        pi = policy(s).squeeze(0)
        #best_action = torch.argmax(pi)
        
        possible_action = env.get_all_actions()
        best_action = possible_action[0]

        for action in possible_action:
            if pi[action] > pi[best_action]:
                best_action = action
        """

        turn *= -1
       
        _, _, terminate = env.step(best_action)
        if terminate:
            if player[turn] == policy:
                policy_win += 1
            if player[turn] == opponent:
                opponent_win += 1
        #env.show_current_board()
    
    return policy_win, opponent_win

def multi_play(policy_model_name: str, opponent_model_name: str, round_: int, n: int):
    policy = load_model(f"./python_main_Env/{policy_model_name}.pth", n)
    opponent = load_model(f"./python_main_Env/{opponent_model_name}.pth", n)
    round = round_
    policy_wins = 0
    opponent_wins = 0

    for _ in tqdm(range(round)):
        policy_win, opponent_win = play(policy, opponent)
        policy_wins += policy_win
        opponent_wins += opponent_win
        
    print(f"policy win: {policy_wins}/{round}")
    print(f"opponent win: {opponent_wins}/{round}")


multi_play("bestModel", "model/policyNetwork_pretrain", 100, 5)
