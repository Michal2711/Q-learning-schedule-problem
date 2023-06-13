import os
import json
import random


EXAMPLES_NUM = 100


def generate_slots():
    slots = []
    for i in range(5):
        day_slot = random.randint(0, 5)
        if day_slot == 5:
            slots.append(day_slot+i*6)
            slots.append(day_slot+i*6-1)
        else:
            slots.append(day_slot+i*6)
            slots.append(day_slot+i*6+1)
    return sorted(slots)


cwd = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.join(cwd, '..', 'data', 'examples')
people_dir = os.path.join(cwd, '..', 'data', 'people')
obrony_dir = os.path.join(cwd, '..', 'data', 'obrony')

workers_file = os.path.join(people_dir, 'workers.json')
obrony_file = os.path.join(obrony_dir, 'obrony.json')

workers = []
obrony = []

with open(workers_file, 'r', encoding='utf-8') as infile:
    workers = json.load(infile)

with open(obrony_file, 'r', encoding='utf-8') as infile:
    obrony = json.load(infile)

for i in range(EXAMPLES_NUM):
    availability = []
    done_dict = {}
    for obrona in obrony:
        promotor = obrona['promotor']
        recenzent = obrona['recenzent']
        if promotor not in done_dict and recenzent not in done_dict:
            slots = generate_slots()
            availability.append([promotor, slots])
            availability.append([recenzent, slots])
            done_dict[promotor] = slots
            done_dict[recenzent] = slots
        elif promotor not in done_dict:
            availability.append([promotor, done_dict[recenzent]])
            done_dict[promotor] = done_dict[recenzent]
        elif recenzent not in done_dict:
            availability.append([recenzent, done_dict[promotor]])
            done_dict[recenzent] = done_dict[promotor]

    # print(availability)

    # availability = [[worker, generate_slots()] for worker in workers]

    # exit()
    output_dir = os.path.join(examples_dir, f'{i}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_name = os.path.join(output_dir, 'availability.json')
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(availability, outfile, indent=1)
