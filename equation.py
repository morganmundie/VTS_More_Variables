class Equation:
    def __init__(self, name):
        self.name = name

    def get_value(self, dt):
        raise NotImplementedError("Subclasses must implement this method")
