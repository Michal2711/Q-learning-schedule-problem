from State_action import Action
import numpy as np
from collections import defaultdict

class Qlearning():
    def __init__(self, env):
        self.Q_table = defaultdict(float)
        self.num_episodes = 1000
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9
        self.env = env

    def qlearning_algorithm(self):
        for episode in range(self.num_episodes):
            # Initialize state
            # state - defence, available_slots, available_chairmans, available_members
            state = self.env.get_initial_state()

            for _ in range(30):  # assume each episode has 100 steps
                defence = state.defence
                available_slots = state.available_slots
                available_chairmans = state.available_chairmans
                available_members = state.available_members

                if np.random.rand() < self.epsilon or (state, 'Exploit') not in self.Q_table:
                    # Exploration: choose random action
                    if not available_chairmans or not available_members or not available_slots:
                        # print(f'No members or chairmans or slots available')
                        break
                        slot = None
                        chairman = None
                        member = None
                    else:
                        slot = np.random.choice(available_slots)
                        chairman = np.random.choice(available_chairmans)
                        member = np.random.choice(available_members)
                else:
                    # Exploitation: choose best action based on current estimate
                    action = self.Q_table[(state, 'Exploit')]
                    slot = action.slot
                    chairman = action.chairman
                    member = action.member

                action = Action(slot, chairman, member)

                # Take action
                next_state, reward = self.env.take_action(state, action)

                if next_state is None or reward is None:
                    print('Episode finished.')
                    break

                # Update Q-table

                old_value = self.Q_table[(state, action)] if self.Q_table[(state, action)] else 0

                available_slots = next_state.available_slots
                available_chairmans = next_state.available_chairmans
                available_members = next_state.available_members
                if available_chairmans and available_members and available_slots:
                    max_next_value = 0
                    for member in available_members:
                        for chairman in available_chairmans:
                            for slot in available_slots:
                                    new_action = Action(slot, chairman, member)
                                    max_next_value = max(max_next_value, self.Q_table.get((next_state, new_action), 0))
                else:
                    max_next_value = 0

                self.Q_table[(state, action)] = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * max_next_value)

                if next_state.defence is None:
                    break

                state = next_state
        return self.Q_table

    def actions(self, state):
        available_slots = state.available_slots
        available_chairmans = state.available_chairmans
        available_members = state.available_members
        possible_actions = [Action(slot, chairman, member) for slot in available_slots for chairman in available_chairmans for member in available_members]
        return possible_actions

    def create_schedule(self):
        # Get the list of actions
        state = self.env.get_initial_state()
        schedule = []
        count = 0
        for i in range(30):
            # print(i)
            # Get the list of actions
            available_actions = self.actions(state)

            # Check if the list of actions is empty
            if not available_actions:
                # Break the loop if there are no available actions
                count += 1
                # print('No available actions for current state.')
                continue

            # Choose best action according to Q-table
            best_action = None
            best_q_value = -float('inf')
            for action in available_actions:
                if self.Q_table[(state, action)] > best_q_value:
                    best_action = action
                    best_q_value = self.Q_table[(state, action)]

            # If best_action is still None, assign a random action
            if best_action is None:
                best_action = np.random.choice(available_actions)

            old_state = state

            # Perform action and observe new state
            state, reward = self.env.take_action(state, best_action)

            # Add action to schedule
            if reward > 0:
                schedule.append((old_state.defence, best_action, reward))

            else:
                count += 1

        return schedule, count