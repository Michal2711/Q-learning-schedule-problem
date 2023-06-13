import matplotlib.pyplot as plt
import json
import pandas as pd
import os


def display_result_schedule(example_path):
    cwd = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(cwd, '..', example_path, 'qlearning_results.json')
    time_slots_dir = os.path.join(cwd, '../data/slots/time_slots.json')
    with open(time_slots_dir) as f:
        slot_time = json.load(f)
    with open(examples_dir) as f:
        schedules = json.load(f)

    timetable = pd.DataFrame(schedules)
    timetable['numer slotu'] = timetable['numer slotu'].astype(str).map(slot_time)
    timetable['Obrona'] = timetable['student']+'\n'+timetable['promotor']

    slot_describtion = pd.DataFrame(timetable['numer slotu'].str.split('-', expand=True))
    slot_describtion['Time'] = slot_describtion[1] + '-' + slot_describtion[2]
    slot_describtion = slot_describtion.drop([1, 2], axis=1)
    slot_describtion = slot_describtion.rename(columns={0: 'Day'})

    desired_order = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
    timetable[['Day', 'Time']] = slot_describtion
    timetable = timetable.pivot(index='Time', columns='Day', values='Obrona')
    timetable = timetable.reindex(columns=desired_order)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.axis('off')
    table = ax.table(cellText=timetable.values,
                     colLabels=timetable.columns,
                     rowLabels=timetable.index,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 3)

    plt.show()
