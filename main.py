import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from Classes import Dataset, Slot, Defence
from Enviroment import Environment
from Qlearning import QLearning
from SARSA import SARSA
from RLexperiment import RLExperiment


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

    sorted_data = sorted(q_experiment.get_schedule_json(), key=lambda x: x['numer slotu'])
    with open(os.path.join(example_path, 'qlearning_results.json'), 'w', encoding='utf-8') as outfile:
        json.dump(sorted_data, outfile, indent=1)

    # SARSA
    sarsa_env = Environment(defences, slots, chairman, members, availability, chairman_avail)
    sarsa_agent = SARSA()

    sarsa_experiment = RLExperiment(sarsa_env, sarsa_agent, num_episodes=10000, max_steps_per_episode=30)
    sarsa_experiment.run()

    sorted_data = sorted(sarsa_experiment.get_schedule_json(), key=lambda x: x['numer slotu'])
    with open(os.path.join(example_path, 'sarsa_results.json'), 'w', encoding='utf-8') as outfile:
        json.dump(sorted_data, outfile, indent=1)


exit()
# load workload data
with open("data/slots/time_slots.json") as f:
    slot_time = json.load(f)

# load timetable data
with open("test.json") as f:
    schedules = json.load(f)

# convert to dataframe
df = pd.DataFrame(schedules)

# map slot number to time slot
df['numer slotu'] = df['numer slotu'].astype(str).map(slot_time)

df['Obrona'] = df['student']+'\n'+df['promotor']

ee = pd.DataFrame(df['numer slotu'].str.split('-', expand=True))
ee['Time'] = ee[1] + '-' + ee[2]
ee = ee.drop([1, 2], axis=1)
ee = ee.rename(columns={0: 'Day'})
# print(ee)
# extract day and time to new columns
df[['Day', 'Time']] = ee

# pivot to create timetable
timetable = df.pivot(index='Time', columns='Day', values='Obrona')

desired_order = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']

# Select columns in desired order
timetable = timetable.reindex(columns=desired_order)

fig, ax = plt.subplots(1, 1)

# Remove axis
ax.axis('off')

# Add a table
table = ax.table(cellText=timetable.values,
                 colLabels=timetable.columns,
                 rowLabels=timetable.index,
                 cellLoc = 'center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2) # you can set the scale according to your specific needs

plt.show()
