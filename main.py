import os
import json
from src.Classes import Dataset, Slot, Defence
from src.Enviroment import Environment
from src.Qlearning import QLearning
from src.SARSA import SARSA
from src.RLexperiment import RLExperiment
from src.utils import display_result_schedule


# Przygotowywanie danych o slotach
with open('data/slots/time_slots.json', 'r') as f:
    slots_data = json.load(f)
slots = [Slot(index, time) for index, time in slots_data.items()]

# Przygotowywanie danych o obronach
with open('data/obrony/obrony.json', 'r') as f:
    defences_data = json.load(f)
defences = [Defence(defence_data["student"], defence_data["promotor"], defence_data["recenzent"]) for defence_data in defences_data]

# Przygotowywanie przykładów
examples_folder_path = 'data/examples'
file_names = os.listdir(examples_folder_path)
sorted_file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
examples_paths_list = [os.path.join(examples_folder_path, file_name) for file_name in sorted_file_names]

for example_path in examples_paths_list[:2]:
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

    # Zapisywanie do plików

    # sorted_data = sorted(q_experiment.get_schedule_json(), key=lambda x: x['numer slotu'])
    # with open(os.path.join(example_path, 'qlearning_results.json'), 'w', encoding='utf-8') as outfile:
    #     json.dump(sorted_data, outfile, indent=1)

    # SARSA
    sarsa_env = Environment(defences, slots, chairman, members, availability, chairman_avail)
    sarsa_agent = SARSA()

    sarsa_experiment = RLExperiment(sarsa_env, sarsa_agent, num_episodes=10000, max_steps_per_episode=30)
    sarsa_experiment.run()

    # Zapisywanie do plików

    # sorted_data = sorted(sarsa_experiment.get_schedule_json(), key=lambda x: x['numer slotu'])
    # with open(os.path.join(example_path, 'sarsa_results.json'), 'w', encoding='utf-8') as outfile:
    #     json.dump(sorted_data, outfile, indent=1)

display_result_schedule(examples_paths_list[9])
