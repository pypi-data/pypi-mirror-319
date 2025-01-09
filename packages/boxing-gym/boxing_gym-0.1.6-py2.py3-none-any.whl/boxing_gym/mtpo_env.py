"""GymNESium environment for Mike Tyson's Punch Out!!"""

import time
import random
import numpy as np
import gymnasium as gym
from gymnesium import NESEnv

# Define NES input constants
NES_INPUT_RIGHT = 0x01
NES_INPUT_LEFT = 0x02
NES_INPUT_DOWN = 0x04
NES_INPUT_UP = 0x08
NES_INPUT_START = 0x10
NES_INPUT_SELECT = 0x20
NES_INPUT_B = 0x40
NES_INPUT_A = 0x80

# Dictionary to map fight_id to the name of the opponent
FIGHT_DICT = {
    0: "Glass Joe",
    1: "Von Kaiser",
    2: "Piston Honda (1)",
    3: "Don Flamenco (1)",
    4: "King Hippo",
    5: "Great Tiger",
    6: "Bald Bull (1)",
    7: "Piston Honda (2)",
    8: "Soda Popinski",
    9: "Bald Bull (2)",
    10: "Don Flamenco (2)",
    11: "Mr. Sandman",
    12: "Super Macho Man",
    13: "Mike Tyson"
}

class PunchOutEnv(NESEnv):
    """An environment for playing Mike Tyson's Punch Out!! with OpenAI Gym."""

    def __init__(self, rom_path:str, headless:bool = False, fps_limit:int = -1) -> None:
        """
        Initialize a new MTPO environment.

        Args:
            rom_path (str): The path to the ROM file.
            headless (bool): Whether to run the emulator in headless mode. Defaults to false
            fps_limit (int): The frame rate limit of the game, negative values are unlimited. Defaults to -1
        
        Returns:
            None
        """
        super().__init__(rom_path, headless=headless)

        self.fps_limit = fps_limit
        self.reward_range = (-float(30), float(30))

        # Define the actions which correspond to: no action, super punch, dodge left, left punch, left uppercut and block.
        self._action_map = [0, NES_INPUT_START, NES_INPUT_LEFT, NES_INPUT_B, NES_INPUT_B | NES_INPUT_UP, NES_INPUT_DOWN]
        self.action_space = gym.spaces.Discrete(len(self._action_map))

        # Choose a fight to begin at.
        self.first_fight = 0 #random.randint(0, 4)

        # Initialise additional variables
        self._time_last = 0
        self._mac_hp_last = 0
        self._opp_down_count_last = 0
        self._opp_hp_last = 0
        self._opp_id_last = 0
        self.was_hit = False
        self.last_time = time.time()
    
    def step(self, action: int):
        ''' Advances one frame of gameplay with a given action. '''
        if self.done: raise ValueError('Cannot step in a done environment! Call `reset` first.')
        
        # If match has started and no save exists, make one
        if self._time != 0 and not self._has_backup:
            self._backup()

        self.nes.controller = self._action_map[action]
        frame = self.nes.step(frames=1)
        obs = np.array(frame, dtype=np.uint8)
        reward = float(self.get_reward())
        self.done = bool(self._get_done())

        if not self._in_fight: self.skip_between_rounds()

        # Bound the reward in [min, max]
        if reward < self.reward_range[0]: reward = self.reward_range[0]
        elif reward > self.reward_range[1]: reward = self.reward_range[1]

        if self.fps_limit > 0:
            # Sleep until the required frame duration has passed for consistent frame rate
            if (1/self.fps_limit - (time.time() - self.last_time)) > 0:
                time.sleep(1/self.fps_limit - (time.time() - self.last_time))
            self.last_time = time.time()

        return obs, reward, self.done, False, {}


    # == RAM VALUES ==
    
    @property
    def _in_fight(self) -> np.uint8:
        '''Return the current round number.'''
        return self.ram[0x0004] == 0xFF
    
    @property
    def _round(self) -> np.uint8:
        '''Return the current round number.'''
        return self.ram[0x0006]
    
    @property
    def _opp_id(self) -> np.uint8:
        '''Return the current fight id.'''
        return self.ram[0x0001]
    
    @property
    def _mac_health(self) -> np.uint8:
        '''Return the Mac's current HP'''
        return self.ram[0x0391]

    @property
    def _opp_health(self) -> np.uint8:
        '''Return the opponant's current HP'''
        return self.ram[0x0398]
    
    @property
    def _mac_down_count(self) -> np.uint8:
        '''Return the number of times Mac has been knocked down'''
        return self.ram[0x03D0]
    
    @property
    def _opp_down_count(self) -> np.uint8:
        '''Return the number of times opponant has been knocked down'''
        return self.ram[0x03D1]

    @property
    def _time(self) -> np.uint16:
        """Return the time left (0 to 999)."""
        # time is represented as a figure with 3 10's places
        return 60*self.ram[0x0302] + 10*self.ram[0x0304] + self.ram[0x0305]

    def _frame_advance(self, action):
        if self.fps_limit > 0:
            start_time = time.time()
            super()._frame_advance(action)
            if 1/self.fps_limit - (time.time() - start_time) > 0: time.sleep(1/self.fps_limit - (time.time() - start_time))
        else:
            super()._frame_advance(action)

    def skip_between_rounds(self) -> None:
        ''' If agent is not in fight then spam start until the next round begins.'''
        while (not self._in_fight) or self._time == self._time_last or self._time == 0:
            if not self._has_backup: self.ram[0x0001] = self.first_fight

            self._frame_advance(0)
            self._frame_advance(0)
            self._frame_advance(NES_INPUT_START)
            self._frame_advance(NES_INPUT_START)


    # == REWARD ==

    @property
    def _health_penalty(self) -> np.uint8:
        """Return the change in Mac's health (a negative value when hp is lost)."""
        _reward = self._mac_health - self._mac_hp_last
        self.was_hit = (_reward != 0)
        self._mac_hp_last = self._mac_health
        return _reward
    
    @property
    def _hit_reward(self) -> np.uint8:
        """Return how much hp the opponent lost in the last frame (positive when opponent loses hp)."""
        _reward = self._opp_hp_last - self._opp_health
        self._opp_hp_last = self._opp_health
        return _reward
    
    @property
    def _ko_reward(self) -> np.uint8:
        """Return a reward if the opponent is knocked down."""
        _reward = self._opp_down_count != self._opp_down_count_last
        self._opp_down_count_last = self._opp_down_count
        return int(_reward)
    
    @property
    def _next_opp_reward(self) -> np.uint8:
        """Return the reward for advancing to the next opponent."""
        _reward =  self._opp_id > self._opp_id_last
        self._opp_id_last = self._opp_id
        return _reward

    @property
    def _time_penalty(self) -> np.uint8:
        """Return the penalty for the in-game clock ticking."""
        _reward = self._time_last - self._time
        self._time_last = self._time

        # time can only decrease, a positive reward results from a reset and should default to 0
        if _reward > 0: return 0

        return _reward

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        self._time_last = 0
        self._mac_hp_last = 0
        self._opp_down_count_last = 0
        self._opp_hp_last = 0
        self._opp_id_last = 0
        self.ram[0x0001] = random.randint(0,5)

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        self._time_last = self._time
        self._mac_hp_last = self._mac_health
        self._opp_down_count_last = self._opp_down_count
        self._opp_hp_last = self._opp_health
        self._opp_id_last = self._opp_id

    def get_reward(self) -> float:
        """Return the reward after a step occurs."""
        return (15*self._next_opp_reward) + (self._time_penalty)*0.1 + (2*self._ko_reward) + self._hit_reward + self._health_penalty

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        # return self._mac_down_count > 0 or self._round > 1
        return self.was_hit

    def _get_info(self):
        """Return the info after a step occurs"""
        return {}
    
    def close(self):
        if not self.headless: self.nes.close()
        return super().close()