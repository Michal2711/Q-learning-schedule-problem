from copy import deepcopy as copy


class RLExperiment:
    def __init__(self, env, agent, num_episodes, max_steps_per_episode):
        self.env = env
        self.agent = agent
        self.num_episodes = num_episodes
        self.max_steps_per_episode = max_steps_per_episode
        self.schedule = []

    def run(self):
        for episode in range(self.num_episodes):
            state = self.env.get_initial_state()

            for step in range(self.max_steps_per_episode):
                possible_actions = self.env.get_possible_actions(state)
                action = self.agent.choose_action(state, possible_actions)

                next_state, reward = self.env.take_action(state, action)

                # Zapisujemy stan i akcję wykonaną do późniejszej wizualizacji
                if state is not None and action:
                    self.schedule.append((state, action))

                next_possible_actions = self.env.get_possible_actions(next_state) if next_state is not None else []
                self.agent.update_q_table(state, action, reward, next_state, next_possible_actions)

                state = next_state

                # Kończymy epizod jeśli nie ma następnego stanu
                if next_state is None:
                    break

    def get_schedule_json(self):
        schedule = []
        defence_slot = {}
        for state, action in self.schedule:
            defence_slot['student'] = state.defence.student
            defence_slot['promotor'] = state.defence.promoter
            defence_slot['recenzent'] = state.defence.reviewer
            defence_slot['przewodniczący'] = self.env.get_chairman_from_slot(action.slot)
            defence_slot['członek komisji'] = action.member
            defence_slot['numer slotu'] = action.slot
            schedule.append(copy(defence_slot))
        return schedule
