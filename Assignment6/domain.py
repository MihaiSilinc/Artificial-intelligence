

class Data:
    def __init__(self, values: list, real_value):

        self.values = values
        self.real_value = real_value
        self.estimated_value = None

class Centroid:
    def __init__(self, values: list, centroid_type):

        self.values = values
        self.centroid_type = centroid_type

