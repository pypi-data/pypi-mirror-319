import abc

class Value(abc.ABC):
    @abc.abstractmethod
    def out(self):
        pass

    @abc.abstractmethod
    def sum(self):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @staticmethod
    def parse(string: str):
        string = string.strip()
        if string.startswith("(") and string.endswith(")"):
            string = string[1:-1]
        balance = 0
        coma = -1
        for i in range(len(string)):
            if string[i] == "(":
                balance += 1
            elif string[i] == ")":
                balance -= 1
            elif balance == 0 and string[i] == ",":
                coma = i
                break
        if coma == -1:
            try:
                return Atom(float(string))
            except:
                print("Ошибка: недопустимое число")
                return None
        else:
            left = Value.parse(string[:coma].strip())
            right = Value.parse(string[coma + 1:].strip())
            if left is None or right is None:
                return None
            return Pair(left, right)

class Atom(Value):
    def __init__(self, number):
        self.number = number

    def out(self):
        print(self.number, end="")

    def sum(self):
        return self.number

    def all(self):
        return [self.number]

class Pair(Value):
    def __init__(self, left: Value, right: Value):
        self.left = left
        self.right = right

    def out(self):
        print('(', end='')
        self.left.out()
        print(", ", end='')
        self.right.out()
        print(')', end='')

    def sum(self):
        return self.left.sum() + self.right.sum()

    def all(self):
        return self.left.all() + self.right.all()

def average(value):
    atoms = value.all()
    if len(atoms) == 0:
        return 0
    return sum(atoms) / len(atoms)

def getDeviation(value):
    atoms = value.all()
    avg = average(value)
    deviations = [abs(atom - avg) for atom in atoms]
    return min(deviations), max(deviations)

