stats = {}


class Stat:
    def __init__(self):
        self.data = []
        self.value = 0
        self.average = 0

    def add_data(self, value):
        self.data.append(value)
        self.value += value
        self.average = self.value / len(self.data)


def add_stat(name, value):
    if name in stats:
        stats[name].add_data(value)
    else:
        stats[name] = Stat()
        stats[name].add_data(value)


def reset_module():
    stats = {}
