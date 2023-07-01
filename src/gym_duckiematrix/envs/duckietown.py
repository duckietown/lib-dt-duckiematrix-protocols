from typing import Dict, List, Tuple, Union
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from dt_duckiematrix_protocols import Matrix
from dt_duckiematrix_protocols.robot.robots import DifferentialDriveRobot
from turbojpeg import TurboJPEG

DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480


class DuckietownEnv(gym.Env):
    
    jpeg = TurboJPEG()

    def __init__(self, entities : Tuple = ('map_0/vehicle_0',), matrix_hostname : str = "localhost", **kwargs):
        """Duckietown environment for OpenAI Gym to control multiple robots in a single Duckiematrix environment.

        Args:
            entities (Tuple, optional): _description_. Defaults to ('map_0/vehicle_0',).
            matrix_hostname (str, optional): _description_. Defaults to "localhost".
        """
        # create connection to the matrix engine
        matrix = Matrix(matrix_hostname, auto_commit=True)

        # get a tuple of robots we want to control
        self.entities : Tuple = entities
        # TODO: [DTSW-3640] check that the entities are all present in the map
        
        # Create a Tuple action space
        base_action_space = spaces.Box(low=np.array([-1, -1]), high=np.array([1, 1]), dtype=np.float32)
        self.action_space = spaces.Tuple([base_action_space]*len(self.entities))

        # Create a Tuple observation space (one for each robot)
        base_observation_space = spaces.Box(
            low=0, high=255, shape=(DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_WIDTH, 3), dtype=np.uint8
        )
        self.observation_space = spaces.Tuple([base_observation_space]*len(self.entities))

        # create connection to the vehicle
        self.robots : Tuple[DifferentialDriveRobot] = tuple(matrix.robots.DB21M(entity) for entity in self.entities)
    
    def step(self, actions : Union[List, Tuple]) -> Tuple[Tuple, Tuple, Tuple, Tuple]:
    
        """Stepping the environment

        Args:
            actions (Union[List, Tuple]): The actions to take for each robot, with each 
                                           action being a Tuple of (left, right) wheel speeds.
        """
        self.latest_actions = actions
        
        for robot, action in zip(self.robots, actions):
            with robot.session():
                robot.drive(left = action[0], right = action[1])
        obs = self._get_image_obs()

        terminated = truncated = False
        info = self._get_info()
        reward = self._get_reward()

        return obs, reward, terminated, truncated, info        
    
    def reset(self):

        for robot in self.robots:
            robot.pose.x = np.random.uniform(-3, 3)
            robot.pose.y = np.random.uniform(-3, 3)
            robot.pose.yaw = np.random.uniform(-np.pi, np.pi)
            robot.pose.update()

        return self._get_image_obs(), self._get_info()
            
    def render(self):
        pass
    
    def close(self):
        pass

    # TODO: [DTSW-3643] fix _get_image_obs returning a blank image
    def _get_image_obs(self) -> Tuple:
        """Get the observations for each robot in the environment

        Returns:
            Tuple: A tuple of one observation for each robot
        """
        rgb_images : List = []

        for robot in self.robots:
            # get frame as compressed frame
            cframe = robot.camera.capture(block=True)
            # get frame as uint8 array
            jpg = cframe.as_uint8()
            bgr = self.jpeg.decode(jpg)
            # bgr -> rgb
            rgb = bgr[:, :, [2, 1, 0]]

            rgb_images.append(rgb)

        return tuple(rgb_images)
    
    # TODO: [DTSW-3644] make _get_info return all matrix yaml files as dictionary
    def _get_info(self) -> Dict:
        """Get the info for each robot in the environment

        Returns:
            info (Dict): A info dictionary with info for each robot
        """
        info : Dict = {}

        for robot, entity_name in zip(self.robots, self.entities):
            info[entity_name] = {
                "position": {
                    "x": robot.pose.x,
                    "y": robot.pose.y,
                    "z": robot.pose.z,
                },
                "orientation": {
                    "roll": robot.pose.roll,
                    "pitch": robot.pose.pitch,
                    "yaw": robot.pose.yaw,
                },
                "velocity": None,
                "angular_velocity": None,
                "battery": None,
                "ground_truth": None,
            }
        
        return info
    # TODO: [DTSW-3598]
    def _get_reward(self) -> float:
        """Get the reward for each robot in the environment"""
        rewards_dict = self._get_entities_rewards()
        return sum(rewards_dict.values())
    
    def _get_entities_rewards(self) -> Dict[str, float]:
        """Get the reward for each entity in the environment"""
        keys = self.entities
        values = [0.0] * len(self.entities)
        return dict(zip(keys, values))