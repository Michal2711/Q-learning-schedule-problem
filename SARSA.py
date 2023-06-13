import random
from collections import defaultdict


class SARSA:
    def __init__(self, alpha=0.5, gamma=0.95, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state, possible_actions):
        if not possible_actions:
            return None
        if random.uniform(0, 1) < self.epsilon:
            # Eksploracja
            return random.choice(possible_actions)
        else:
            # Eksploatacja
            q_values = {action: self.q_table[str(state)][str(action)] for action in possible_actions}
            return max(q_values, key=q_values.get)

    def update_q_table(self, state, action, reward, next_state, next_possible_actions):
        if next_state is not None:
            next_action = self.choose_action(next_state, next_possible_actions)
            td_target = reward + self.gamma * self.q_table[str(next_state)][str(next_action)]
        else:
            td_target = reward
        td_error = td_target - self.q_table[str(state)][str(action)]
        self.q_table[str(state)][str(action)] += self.alpha * td_error
