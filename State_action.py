class State:
    def __init__(self, defence, available_slots, available_chairmans, available_members):
        self.defence = defence
        self.available_slots = available_slots
        self.available_chairmans = available_chairmans
        self.available_members = available_members

    def __hash__(self) -> int:
        return hash((self.defence, tuple(self.available_slots), tuple(self.available_chairmans), tuple(self.available_members)))

    def __eq__(self, other):
        return (self.defence, self.available_slots, self.available_chairmans, self.available_members) == (other.defence, other.available_slots, other.available_chairmans, other.available_members)

    def __str__(self):
        return (f'State: \n \t {self.defence}\n\t available_slots: {self.available_slots}\n\t available_chairmans: {self.available_chairmans}\n\t available_members: {self.available_members}')

class Action:
    def __init__(self, slot, chairman, member):
        self.slot = slot
        self.chairman = chairman
        self.member = member

    def __hash__(self) -> int:
        return hash((self.slot, self.chairman, self.member))

    def __eq__(self, other):
        return (self.slot, self.chairman, self.member) == (other.slot, other.chairman, other.member)

    def __str__(self):
        return (f'Action: \n \t Picked slot: {self.slot} \n \t Picked chairman: {self.chairman} \n \t Picked_member: {self.member}')