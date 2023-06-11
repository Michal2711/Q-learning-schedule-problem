import math
from State_action import State

class Environment():
    def __init__(self, defences, slots, chairmans, members, availability):
        self.defences = defences
        self.slots = slots
        self.chairmans = chairmans
        self.members = members
        self.availability = availability

    def get_initial_state(self):
        self.all_slots = [i for i in range(30)]
        # if /6 are equal it means that it's the same day
        promoter = self.defences[0].promoter
        reviewer = self.defences[0].reviewer
        available_slots_promoter = self.availability[promoter]
        available_slots_reviewer = self.availability[reviewer]
        available_slots = available_slots_promoter + available_slots_reviewer
        available_slots = list(set(self.all_slots) & set(available_slots))
        available_chairmans = []
        available_members = []
        for slot in available_slots:
            for chairman in self.chairmans:
                if math.floor(slot / 6) == math.floor(self.availability[chairman][0] / 6):
                    available_chairmans.append(chairman)
            for member in self.members:
                if slot in self.availability[member]:
                    available_members.append(member)

        available_chairmans = list(set(available_chairmans))
        available_members = list(set(available_members))

        available_chairmans = list(filter(lambda x: x!= promoter, available_chairmans))
        available_chairmans = list(filter(lambda x: x!= reviewer, available_chairmans))
        available_members = list(filter(lambda x: x!= promoter, available_members))
        available_members = list(filter(lambda x: x!= reviewer, available_members))

        # print(available_slots)

        return State(self.defences[0], available_slots, available_chairmans, available_members)

    def get_reward(self, defence, slot, chairman, member):
        if chairman in self.chairmans and member in self.members and \
           slot // 6 == self.availability[chairman][0] // 6 and slot in self.availability[member] and \
            (slot in self.availability[defence.promoter] or slot in self.availability[defence.reviewer]):
            return 1
        else:
            return -1

    # def get_reward(self, defence, slot, chairman, member):
    #     if slot in self.availability[chairman] and slot in self.availability[member] and \
    #         slot in self.availability[defence.promoter] + self.availability[defence.reviewer]:
    #         return 1
    #     else:
    #         return -1

    def take_action(self, state, action):
        # Unpack state and action
        defence = state.defence
        available_slots = state.available_slots
        available_chairmans = state.available_chairmans
        available_members = state.available_members

        slot = action.slot
        chairman = action.chairman
        member = action.member

        # Check if the action is valid
        if chairman not in available_chairmans or member not in available_members or slot not in available_slots:
            return state, -1

        reward = self.get_reward(defence, slot, chairman, member)

        # Update lists of available chairmans and members
        # available_chairmans.remove(chairman)
        # available_members.remove(member)
        # available_slots.remove(slot)
        self.all_slots.remove(slot)

        # Move to the next defence and slot
        if self.defences.index(defence) < len(self.defences) - 1:
            next_defence = self.defences[self.defences.index(defence) + 1]

            # Update lists of available chairmans and members
            promoter = next_defence.promoter
            reviewer = next_defence.reviewer
            available_slots_promoter = self.availability[promoter]
            available_slots_reviewer = self.availability[reviewer]
            available_slots = available_slots_promoter + available_slots_reviewer
            available_slots = list(set(self.all_slots) & set(available_slots))
            available_chairmans = []
            available_members = []

            for slot in available_slots:
                for chairman in self.chairmans:
                    if math.floor(slot / 6) == math.floor(self.availability[chairman][0] / 6):
                    # if slot in self.availability[chairman]:
                        available_chairmans.append(chairman)
                for member in self.members:
                    if slot in self.availability[member]:
                        available_members.append(member)

            available_chairmans = list(set(available_chairmans))
            available_members = list(set(available_members))

            available_chairmans = list(filter(lambda x: x!= promoter, available_chairmans))
            available_chairmans = list(filter(lambda x: x!= reviewer, available_chairmans))
            available_members = list(filter(lambda x: x!= promoter, available_members))
            available_members = list(filter(lambda x: x!= reviewer, available_members))

            # print(available_slots)

            # Update state
            next_state = State(next_defence, available_slots, available_chairmans, available_members)

            # Get reward
            # reward = self.get_reward(defence, slot, chairman, member)
        else:
            next_defence = None
            next_state = None
            reward = None
            return next_state, reward

        return next_state, reward