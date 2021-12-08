stats = []
stats_average = []

# Ajoute une valeur à une statistique
def add_stat(name, value):
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
