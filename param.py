from equations.random_wave import RandomWave

class Param:
    def __init__(self, name="Change", wave_type=None, min_val=0, max_val=1):
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
     #update and save? or no   
    def update_param(self):
        print(f"update {self.name}")
