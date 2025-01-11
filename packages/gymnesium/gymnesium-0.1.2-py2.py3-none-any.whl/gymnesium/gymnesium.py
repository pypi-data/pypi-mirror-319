import numpy as np
from cynes import *
from cynes import NES
from cynes.windowed import WindowedNES
import gymnasium as gym
from gymnasium.spaces import Box
from gymnasium.spaces import Discrete
from abc import abstractmethod

# Height and width in pixels of the NES screen
SCREEN_HEIGHT, SCREEN_WIDTH = 240, 256

SCREEN_SHAPE_24_BIT = SCREEN_HEIGHT, SCREEN_WIDTH, 3

class NESRam:
    ''' Class to handle basic RAM reading and writing. '''
    def __init__(self, nes):
        self.nes = nes

    def __getitem__(self, address):
        return self.nes[address]

    def __setitem__(self, address, value):
        self.nes[address] = value

    @property
    def flags_6(self):
        """Return the flags at the 6th byte of the header."""
        return '{:08b}'.format(self.header[6])
    
    @property
    def header(self):
        """Return the header of the ROM file as bytes."""
        return self.nes[:16]
    
    @property
    def flags_9(self):
        """Return the flags at the 9th byte of the header."""
        return '{:08b}'.format(self.header[9])
    
    @property
    def prg_rom_size(self):
        """Return the size of the PRG ROM in KB."""
        return 16 * self.header[4]
    
    @property
    def has_trainer(self):
        """Return a boolean determining if the ROM has a trainer block."""
        return bool(int(self.flags_6[5]))
    
    @property
    def is_pal(self):
        """Return if the TV system this ROM supports is PAL."""
        return bool(int(self.flags_9[7]))


class NESEnv(gym.Env):
    ''' NES Gymnasium Environment. '''

    def __init__(self, rom_path, headless=False) -> None:
        """
        Create a new NES environment.

        Args:
            rom_path (str): The path to the NES .rom file to be loaded.
            headless (bool): Optional - Define whether the environment should run in headless mode with no window, or not.

        Returns:
            None

        """        
        self._ram = NESRam(self.nes)

        # Check the ROM is valid
        if self._ram.prg_rom_size == 0: raise ValueError('ROM has no PRG-ROM banks.')
        if self._ram.has_trainer: raise ValueError('ROM has trainer. trainer is not supported.')
        if self._ram.is_pal: raise ValueError('ROM is PAL. PAL is not supported.')
        
        self._has_backup = False # Initially no state has been saved
        self.done = True # Setup a done flag

        # Create either windowless or windowed instance of the cynes emulator
        self.headless = headless
        self.nes = NES(rom_path) if self.headless else WindowedNES(rom_path)

        # Define observation and action spaces
        self.observation_space = Box(low=0, high=255, shape=(240, 256, 3), dtype=np.uint8)
        self.action_space = Discrete(256)

    @property
    def ram(self):
        return self._ram
    
    def reset(self, seed=None, options=None):
        '''
        Reset the emulator to the last save, or to power on if no save is present.

        Args:
            seed (optional int):    The seed that is used to initialize the parent Gym environment's PRNG (np_random).
            
            options (optional dict): Additional information to specify how the environment is reset (optional)
        '''
        super().reset(seed=seed, options=options)

        # Call the before reset callback
        self._will_reset()

        # Reset the emulator
        if self._has_backup: self._restore()
        else: self.nes.reset()

        # Call the after reset callback
        self._did_reset()

        self.done = False
        obs = self.nes.step(frames=1)  # Capture an initial frame
        obs = np.array(obs, dtype=np.uint8)  # Ensure it's a valid numpy array
        info = {}
        return obs, info

    @abstractmethod
    def step(self, action):
        raise("Step method must be overridden for each game environment.")

    def _backup(self) -> None:
        """Backup the current emulator state."""
        self._backup_state = self.nes.save()
        self._has_backup = True

    def _restore(self) -> None:
        """Restore the emulator state from backup."""
        self.nes.load(self._backup_state)

    def _frame_advance(self, action):
        """
        Advance the emulator by one frame with the given action.

        Args:
            action (int): The action to perform (controller input).
        """
        # Set the controller inputs
        self.nes.controller = action

        # Advance the emulator by one frame
        frame = self.nes.step(frames=1)

        # Update the current frame (observation)
        self.screen = frame

    @abstractmethod
    def _will_reset(self):
        ''' Called just before a reset, can be used to apply any RAM hacking before resetting. '''
        pass
    
    @abstractmethod
    def _did_reset(self):
        ''' Called after a reset, can be used to apply any RAM hacking required after resetting. '''
        pass
