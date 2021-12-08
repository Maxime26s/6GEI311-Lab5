stats = []
list_value = 0
stat_average = []


class Stat:
    def __init__(self):
        self.data = []
        self.value = 0
        self.average = 0

    def add_data(self, value):
        self.data.append(value)
        self.value += value
        self.average = self.value / len(self.data)


# Ajoute une valeur à une statistique
def add_stat(name, value):
    global total_value
    added = False
    valueT = str(value)
    for i in range(len(stats)):
        if stats[i][0] == name:
            stats[i][1] = valueT

            stat_average[i][0] += value
            stat_average[i][1] += 1
            stats[i][2] = stat_average[i][0] / stat_average[i][1]

            added = True

    if added == False:
        stats.append([name, valueT, value])
        stat_average.append([value, 1])
        added = True


# Reset les statistiques
def reset_module():
    stats = {}
