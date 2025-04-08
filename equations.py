import math
import random
# from noise import pnoise1  # pip install noise
# import numpy as np
# from scipy.interpolate import interp1d

class RandomWave:
    """
    A randomized wave pattern
    """
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        
        self.position = 0.0 # starting position of the param
        
        # Initial parameters
        self.freq = 0.05   # current frequency 
        self.amp = 1.0     # current amplitude
        self.target_freq = self.freq
        self.target_amp = self.amp
        
        # Time tracking for random updates (in seconds)
        self.time_since_update = 0.0
        self.update_interval = random.uniform(0.5, 5.0)  # choose random interval between changes

    def update_parameters(self, dt):
        """
        Update target parameters every update_interval seconds.
        dt: time delta (seconds) since last call.
        """
        self.time_since_update += dt
        
        # Change freq and amp and update time 
        if self.time_since_update >= self.update_interval:
            self.time_since_update = 0.0
            # Pick a new random update interval for next time // todo link with above
            self.update_interval = random.uniform(0.5, 5.0)
            # Randomize freq, values near 0 produces a "stop"
            self.target_freq = random.uniform(0, 0.2)
            self.target_amp = random.uniform(0.5, 1.0)
        
        smoothing = 0.05  
        self.freq += (self.target_freq - self.freq) * smoothing
        self.amp  += (self.target_amp - self.amp) * smoothing

    def get_value(self, dt):
        """
        dt: time delta (seconds) to advance
        Returns the current output of the wave.
        """
        self.update_parameters(dt)
        
        # change by speed of 20 //todo make this dynamic
        self.position += self.freq * dt * 20
        
        # Compute the wave output
        return self.amp * math.sin(self.position)
    
    
