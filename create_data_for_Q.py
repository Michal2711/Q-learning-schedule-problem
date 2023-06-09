import json
import os

class Examples_dataset():
    def __init__(self, example):
        self.availability = {}
        # self.base_path = 'data/examples/'
        self.example = example
        self.load_data()

    def load_data(self):
        with open(self.example, 'r') as f:
            self.availability_data = json.load(f)

    def create_availability(self):
        for person, slot_index in self.availability_data:
            if (slot_index + 1) % 6 == 0:
                self.availability[person] = [slot_index - 1, slot_index]
            else:
                self.availability[person] = [slot_index, slot_index + 1]
        return self.availability