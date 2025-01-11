"""GymNESium NES environment for Gymnasium"""
from .gymnesium import NESEnv


# explicitly define the outward facing API of this package
__all__ = [NESEnv.__name__]