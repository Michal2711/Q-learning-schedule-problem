import random
import numpy as np
from collections import defaultdict


class QLearning:
    def __init__(self, learning_rate=0.5, discount_factor=0.95, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state, possible_actions):
        if not possible_actions:
            return None
        if random.uniform(0, 1) < self.exploration_rate:
            # Eksploracja
            return random.choice(possible_actions)
        else:
            # Exploatacja
            q_values = [self.get_q_value(state, action) for action in possible_actions]
            max_q_value_index = np.argmax(q_values)
            return possible_actions[max_q_value_index]

    def get_q_value(self, state, action):
        return self.q_table[state][action]

    def update_q_table(self, state, action, reward, next_state, next_possible_actions):
        if next_state is None:
            max_future_q_value = 0
        else:
            future_q_values = [self.get_q_value(next_state, next_action) for next_action in next_possible_actions]
            max_future_q_value = max(future_q_values)

        old_q_value = self.get_q_value(state, action)
        new_q_value = (1 - self.learning_rate) * old_q_value + self.learning_rate * (reward + self.discount_factor * max_future_q_value)

        self.q_table[state][action] = new_q_value
