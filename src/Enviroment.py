from src.Classes import State, Action
from copy import deepcopy as copy


class Environment():
    def __init__(self, defences, slots, chairman, members, availability, chairman_avail):
        self.defences = defences
        self.slots = slots
        self.chairmans = chairman
        self.members = members
        self.availability = availability
        self.current_avail = copy(availability)
        self.free_slots = [i for i in range(30)]
        self.chairman_avail = chairman_avail

    def get_chairman_from_slot(self, slot):
        for chairman, avail in self.chairman_avail.items():
            if slot in avail:
                return chairman

    def get_avail_slots(self, promoter, reviewer):
        promoter_avail = self.availability[promoter]
        reviewer_avail = self.availability[reviewer]
        avail_slots = list(set(promoter_avail).intersection(set(reviewer_avail)))
        avail_slots = list(set(avail_slots).intersection(set(self.free_slots)))
        return avail_slots

    def get_available_members(self, slots, promoter, reviewer):
        members = []
        for worker, avail in self.current_avail.items():
            if (set(slots) & set(avail)) and worker != promoter and worker != reviewer:
                members.append(worker)
        return members

    def get_initial_state(self):
        defence = self.defences[0]
        promoter = defence.promoter
        reviewer = defence.reviewer

        avail_slots = self.get_avail_slots(promoter, reviewer)
        available_members = self.get_available_members(avail_slots, promoter, reviewer)

        return State(defence, avail_slots, available_members)

    def get_possible_actions(self, state):
        actions = []
        if state is not None:
            for slot in state.available_slots:
                for member in state.available_members:
                    if slot in self.current_avail[member]:
                        actions.append(Action(slot, member))
        return actions

    def get_reward(self, state, action, next_state):
        if action is None:
            reward = -1
        else:
            reward = 1
        return reward

    def get_next_state(self, state):
        if self.defences.index(state.defence) < len(self.defences) - 1:
            next_defence = self.defences[self.defences.index(state.defence) + 1]

            next_promoter = next_defence.promoter
            next_reviewer = next_defence.reviewer

            avail_slots = self.get_avail_slots(next_promoter, next_reviewer)
            available_members = self.get_available_members(avail_slots, next_promoter, next_reviewer)
            if not avail_slots or not available_members:
                next_state = None
            else:
                next_state = State(next_defence, avail_slots, available_members)
        else:
            next_state = None

        return next_state

    def update_availability(self, action):
        chosen_slot = action.slot
        chosen_member = action.member
        self.free_slots.remove(chosen_slot)
        self.current_avail[chosen_member].remove(chosen_slot)

    def take_action(self, state: State, action: Action):
        # Można jeszcze dodać walidację akcji
        if action is not None:
            self.update_availability(action)
        next_state = self.get_next_state(state)
        reward = self.get_reward(state, action, next_state)

        return next_state, reward
