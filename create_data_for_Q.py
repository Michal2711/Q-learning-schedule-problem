import json
import os

class Examples_dataset():
    def __init__(self, example, chairmans):
        self.availability = {}
        # self.base_path = 'data/examples/'
        self.example = example
        self.chairmans = chairmans
        self.load_data()

    def load_data(self):
        with open(self.example, 'r') as f:
            self.availability_data = json.load(f)

    def create_availability(self):
        for person, slot_index in self.availability_data:
            # if person in self.chairmans:
            #     begin = slot_index // 6
            #     end = begin + 5
            #     self.availability[person] = [i for i in range(begin, end+1)]
            # else:
            if (slot_index + 1) % 6 == 0:
                self.availability[person] = [slot_index - 1, slot_index]
            else:
                self.availability[person] = [slot_index, slot_index + 1]
        return self.availability