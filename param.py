from equations.random_wave import RandomWave

class Param:
    def __init__(self, name, wave_type, min_val, max_val):
        self.name = name
        self.wave_type = wave_type
        self.min_val = min_val
        self.max_val = max_val
        self.wave = self._create_wave()

    def _create_wave(self):
        if self.wave_type == "random_wave":
            return RandomWave(self.name)
        else:
            print(f"Error: Wave type wrong")
            return None
