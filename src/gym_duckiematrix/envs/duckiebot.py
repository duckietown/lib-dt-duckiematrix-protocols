import gymnasium as gym
from gymnasium import spaces
import numpy as np
from dt_duckiematrix_protocols import Matrix

class DuckietownEnv(gym.Env):
    
    def __init__(self, gain=1.0, trim=0.0, radius=0.0318, k=27.0, limit=1.0, matrix_hostname : str = "localhost", **kwargs):
        
        self.action_space = spaces.Box(low=np.array([-1, -1]), high=np.array([1, 1]), dtype=np.float32)
        # create connection to the matrix engine
        matrix = Matrix(matrix_hostname, auto_commit=True)
        # get a list of robots we want to control and check that they are all the robots present in the map
        # create connection to the vehicle
        self.robot = matrix.robots.DB21M("map_0/vehicle_0")
        
        # Should be adjusted so that the effective speed of the robot is 0.2 m/s
        self.gain = gain

        # Directional trim adjustment
        self.trim = trim

        # Wheel radius
        self.radius = radius

        # Motor constant
        self.k = k

        # Wheel velocity limit
        self.limit = limit

    def step(self, action):
        # make action a dictionary containing actions for each duckiebot
        pass
    
    def reset(self):
        pass
    
    def render(self):
        pass
    
    def close(self):
        pass