import os
import json
import random


EXAMPLES_NUM = 100


def generate_slots(available_days):
    day = random.choice(available_days)
    day_slots = [i for i in range(day*6, day*6+6)]
    return day_slots, day


cwd = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.join(cwd, '..', 'data', 'examples')
people_dir = os.path.join(cwd, '..', 'data', 'people')

chairmen_file = os.path.join(people_dir, 'przewodniczacy.json')

chairmen = []

with open(chairmen_file, 'r', encoding='utf-8') as infile:
    chairmen = json.load(infile)

for i in range(EXAMPLES_NUM):
    available_days = [i for i in range(5)]
    chairmen_days = []
    for chairman in chairmen[:5]:
        day_slots, day = generate_slots(available_days)
        chairmen_days.append([chairman, day_slots])
        available_days.remove(day)
    output_dir = os.path.join(examples_dir, f'{i}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_name = os.path.join(output_dir, 'chairman.json')
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(chairmen_days, outfile, indent=1)
