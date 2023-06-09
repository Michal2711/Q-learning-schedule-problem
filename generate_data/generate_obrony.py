import json
import random
import os


class Obrona:
    """Klasa umożliwiająca zapis do pliku json"""
    def __init__(self, student=None, promotor=None,
                 recenzent=None, czlonek_komisji=None, prowadzacy=None):
        self.student = student
        self.promotor = promotor
        self.recenzent = recenzent
        self.czlonek_komisji = czlonek_komisji
        self.prowadzacy = prowadzacy


obrony = []
students = []
workers = []

# Przygotowanie ścieżek do plików
cwd = os.path.dirname(os.path.abspath(__file__))

people_dir = os.path.join(cwd, '..', 'data', 'people')
students_file = os.path.join(people_dir, 'students.json')
workers_file = os.path.join(people_dir, 'workers.json')
obrony_file = os.path.join(cwd, '..', 'data', 'obrony', 'obrony.json')

# Odczyt z plików
with open(students_file, 'r', encoding='utf-8') as infile:
    students = json.load(infile)
with open(workers_file, 'r', encoding='utf-8') as infile:
    workers = json.load(infile)


# Przydział losowy promotorów i recenzentów
promotorzy = random.sample(workers, len(students))
recenzenci = random.sample(workers, len(students))

for i in range(len(students)):
    obrony.append(Obrona(students[i], promotorzy[i], recenzenci[i]))

# Zapis do pliku
with open(obrony_file, 'w') as outfile:
    json.dump([obj.__dict__ for obj in obrony], outfile, indent=4)
