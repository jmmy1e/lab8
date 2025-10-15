import abc
import random

class Vehicle(abc.ABC):
    """Abstract base vehicle with shared state and movement behavior."""

    def __init__(self, name, initial, speed):
        self._name = name
        self._initial = initial
        self._speed = speed
        self._position = 0
        self._energy = 100

    # ----- properties -----
    @property
    def initial(self):
        return self._initial

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value < 0:
            value = 0
        self._position = value

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        if value < 0:
            value = 0
        self._energy = value

    # ----- movement methods -----
    def fast(self, obs_loc):
        """
        Fast move:
          - If energy >= 5: spend 5 energy, move (speed ± 1)
          - Else: move 1
          - If an obstacle is in the path: crash and stop on obstacle
        """
        if self.energy >= 5:
            move = random.randint(self._speed - 1, self._speed + 1)
            self.energy = self.energy - 5
        else:
            move = 1

        start = self.position
        end = start + move

        if obs_loc is not None and start < obs_loc <= end:
            self.position = obs_loc
            return self._name + " CRASHED into an obstacle!"
        else:
            self.position = end
            return self._name + " quickly moves " + str(end - start) + " units!"

    def slow(self, obs_loc):
        """
        Slow move:
          - Move at half speed ± 1 (no energy cost)
          - Slow 'goes around' obstacles (no crash)
        """
        half = self._speed // 2
        move = random.randint(half - 1, half + 1)
        if move < 0:
            move = 0

        start = self.position
        end = start + move

        dodged = (obs_loc is not None) and (start < obs_loc <= end)

        self.position = end
        if dodged:
            return self._name + " slowly dodges the obstacle and moves " + str(end - start) + " units!"
        else:
            return self._name + " slowly moves " + str(end - start) + " units!"

    @abc.abstractmethod
    def special_move(self, obs_loc):
        """Subclass-specific special move."""
        pass

    def __str__(self):
        return self._name + " [Position - " + str(self.position + 1) + ", Energy - " + str(self.energy) + "]"
