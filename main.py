import json
import os
import glob
from Classes import Dataset, State, Action, Slot, Defence
from Enviroment import Environment
from Qlearning import QLearning
from SARSA import SARSA
from RLexperiment import RLExperiment

with open('data/slots/time_slots.json', 'r') as f:
    slots_data = json.load(f)

with open('data/obrony/obrony.json', 'r') as f:
    defences_data = json.load(f)

# with open('data/people/przewodniczacy.json', 'r') as f:
#     chairmans = json.load(f)

# with open('data/people/workers.json', 'r') as f:
#     members = json.load(f)


folder_path = 'data/examples'
file_names = os.listdir(folder_path)
sorted_file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
examples_paths_list = [os.path.join(folder_path, file_name) for file_name in sorted_file_names]

defences = [Defence(defence_data["student"], defence_data["promotor"], defence_data["recenzent"]) for defence_data in defences_data]
slots = [Slot(index, time) for index, time in slots_data.items()]

for example_path in examples_paths_list:
    dataset = Dataset(example_path)
    chairman = list(dataset.get_chairman_avail().keys())
    chairman_avail = dataset.get_chairman_avail()
    availability = dataset.get_workers_avail()
    members = list(availability.keys())

    # Q-Learning
    q_env = Environment(defences, slots, chairman, members, availability, chairman_avail)
    q_agent = QLearning()

    q_experiment = RLExperiment(q_env, q_agent, num_episodes=1000, max_steps_per_episode=30)
    q_experiment.run()

    # print(len(q_experiment.schedule))

    if len(q_experiment.schedule) == 30:

        sorted_data = sorted(q_experiment.get_schedule_json(), key=lambda x: x['numer slotu'])
        with open('test.json', 'w', encoding='utf-8') as outfile:
            json.dump(sorted_data, outfile, indent=1)
        exit()

    # # SARSA
    # sarsa_env = Environment(defences, slots, chairman, members, availability, chairman_avail)
    # sarsa_agent = SARSA()

    # sarsa_experiment = RLExperiment(sarsa_env, sarsa_agent, num_episodes=10000, max_steps_per_episode=30)
    # sarsa_experiment.run()

    # if len(sarsa_experiment.schedule) == 30:
    #     print(example_path)


# print(examples_paths_list[0])
# a = Dataset(examples_paths_list[0])
# print(a.get_workers_avail())
# print(a.get_chairman_avail())

# a = Defence(1, 2, 3)
# b = Defence(1, 2, 4)
# print(a == b)

# a = State(1, 2, 3)
# b = State(1, 2, 4)
# print(a == b)

# a = Action(1, 2)
# b = Action(1, 4)
# print(a == b)

# a = Slot(1, 2)
# b = Slot(1, 4)
# print(a == b)
