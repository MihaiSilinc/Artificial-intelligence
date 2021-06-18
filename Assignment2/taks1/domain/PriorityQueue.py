class PriorityQueue:
    def __init__(self):
        self.__values = {}

    def __str__(self):
        out = ''
        for el in self.__values:
            out += str(el)
            out += ':'
            out += str(self.__values[el])
            out += '\n'
        return out[:-1]

    def isEmpty(self):
        return len(self.__values) == 0

    def pop(self):
        topP = None
        topo = None
        for obj in self.__values:
            objPriority = self.__values[obj]
            if topP is None or topP > objPriority:
                topP = objPriority
                topo = obj
        del self.__values[topo]
        return topo, topP

    def push(self, obj, priority):
        self.__values[obj] = priority

    def contains(self, val):
        return val in self.__values

    def getObjPriority(self, obj):
        return self.__values[obj]

    def update(self, key, value):
        self.__values[key] = value


