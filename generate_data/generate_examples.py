import os
import json
import random

EXAMPLES_NUM = 100


cwd = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.join(cwd, '..', 'data', 'examples')
people_dir = os.path.join(cwd, '..', 'data', 'people')

workers_file = os.path.join(people_dir, 'workers.json')

workers = []

with open(workers_file, 'r', encoding='utf-8') as infile:
    workers = json.load(infile)


for i in range(EXAMPLES_NUM):
    availability = [[worker, random.randint(0, 29)] for worker in workers]
    file_name = os.path.join(examples_dir, f'{i}.json')
    with open(file_name, 'w', encoding='utf-8') as outfile:
        json.dump(availability, outfile, indent=1)
