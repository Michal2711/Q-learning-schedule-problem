class Defence:
    def __init__(self, student, promoter, reviewer):
        self.student = student
        self.promoter = promoter
        self.reviewer = reviewer

    def __str__(self):
        return (f'Defence exam: student: {self.student}, promoter: {self.promoter}, reviewer: {self.reviewer}')

class Slot:
    def __init__(self, index, time):
        self.index = index
        self.time = time

    def __str__(self):
        return (f'This is slot {self.index}, {self.time}')
