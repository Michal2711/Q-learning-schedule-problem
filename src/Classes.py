import json
import os


class Dataset():
    def __init__(self, example_path: os.PathLike):
        self.workers_avail = {}
        self.chairman_avail = {}
        chairman_avail_path = os.path.join(example_path, 'chairman.json')
        self.read_chairman_avail(chairman_avail_path)
        workers_avail_path = os.path.join(example_path, 'availability.json')
        self.read_workers_avail(workers_avail_path)

    def read_chairman_avail(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        for chairmen, availability in data:
            self.chairman_avail[chairmen] = availability

    def read_workers_avail(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        for worker, availability in data:
            self.workers_avail[worker] = availability

        # Remove slots when worker is a chairmen
        for chairmen in self.chairman_avail:
            if chairmen in self.workers_avail:
                for avail in self.chairman_avail[chairmen]:
                    if avail in self.workers_avail[chairmen]:
                        self.workers_avail[chairmen].remove(avail)

    def get_workers_avail(self):
        return self.workers_avail

    def get_chairman_avail(self):
        return self.chairman_avail


class State:
    def __init__(self, defence, available_slots, available_members):
        self.defence = defence
        self.available_slots = available_slots
        self.available_members = available_members

    def __hash__(self) -> int:
        return hash((self.defence, tuple(self.available_slots), tuple(self.available_members)))

    def __eq__(self, other):
        if isinstance(other, State):
            return (self.defence, self.available_slots, self.available_members) == (other.defence, other.available_slots, other.available_members)
        raise TypeError(f"Cannot compare class 'State' to '{type(other).__name__}'")

    def __str__(self):
        return (f'State:\n\t{self.defence}\n\tavailable_slots: {self.available_slots}\n\tavailable_members: {self.available_members}')


class Action:
    def __init__(self, slot, member):
        self.slot = slot
        self.member = member

    def __hash__(self) -> int:
        return hash((self.slot, self.member))

    def __eq__(self, other):
        if isinstance(other, Action):
            return (self.slot, self.member) == (other.slot, other.member)
        raise TypeError(f"Cannot compare class 'Action' to '{type(other).__name__}'")

    def __str__(self):
        return (f'Action:\n\tPicked slot: {self.slot}\n\tPicked_member: {self.member}')


class Slot:
    def __init__(self, index, time):
        self.index = index
        self.time = time

    def __eq__(self, other):
        if isinstance(other, Slot):
            return (self.index, self.time) == (other.index, other.time)
        raise TypeError(f"Cannot compare class 'Slot' to '{type(other).__name__}'")

    def __str__(self):
        return (f'This is slot {self.index}, {self.time}')


class Defence:
    def __init__(self, student, promoter, reviewer):
        self.student = student
        self.promoter = promoter
        self.reviewer = reviewer

    def __hash__(self) -> int:
        return hash((self.student, self.promoter, self.reviewer))

    def __eq__(self, other):
        if isinstance(other, Defence):
            return (self.student, self.promoter, self.reviewer) == (other.student, other.promoter, other.reviewer)
        raise TypeError(f"Cannot compare class 'Defence' to '{type(other).__name__}'")

    def __str__(self):
        return (f'Defence exam: student: {self.student}, promoter: {self.promoter}, reviewer: {self.reviewer}')
