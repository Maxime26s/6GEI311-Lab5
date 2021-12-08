stats = []
# list_value = 0
stats_average = []


# class Stat:
#     def __init__(self):
#         self.data = []
#         self.value = 0
#         self.average = 0

#     def add_data(self, value):
#         self.data.append(value)
#         self.value += value
#         self.average = self.value / len(self.data)


# Ajoute une valeur à une statistique
def add_stat(name, value):
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
            
            stats_average[i][0] += value
            stats_average[i][1] += 1
            stats[i][2]  = stats_average[i][0] / stats_average[i][1]

            added = True
    
    if added == False:
        stats.append([name, valueT, value])
        stats_average.append([value, 1])
        added = True 

# Reset les statistiques
def reset_module():
    stats = {}
