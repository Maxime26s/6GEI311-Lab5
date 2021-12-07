stats = []
list_value = 0
state_average = []


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
    # if name in stats:
    #     stats[name].add_data(value)
    # else:
    #     stats[name] = Stat()
    #     stats[name].add_data(value)
    added = False
    valueT = str(value)
    for i in range(len(stats)):
        if stats[i][0] == name:
            stats[i][1] = valueT
            
            # state_average[i][0] += value
            # state_average[i][1] += 1
            # stats[i][2]  = state_average[i][0] / state_average[i][1]

            added = True
    
    if added == False:
        stats.append([name, valueT, value])
        # state_average.append([value, 1])
        added = True 

# Reset les statistiques
def reset_module():
    stats = {}
