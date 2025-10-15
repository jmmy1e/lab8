import abc
import random

class Vehicle(abc.ABC):
    """
    Base class for all vehicles in the race.
    Stores the shared state (name, label, speed, position energy)
    and common move behavior (fast/slow).
    Subclasses only store and need to fill the special move.
    """

    def __init__(self, name, initial, speed):
        """Set up and initialize a new vehicle."""
        self._name = name
        self._initial = initial
        self._speed = speed
        self._position = 0
        self._energy = 100

    # --- Properties ---
    @property
    def initial(self):
        """The letter shown on the track for this vehicle."""
        return self._initial

    @property
    def position(self):
        """Current location on the lane."""
        return self._position

    @position.setter
    def position(self, value):
        """Clamp position to 0 or higher."""
        if value < 0:
            value = 0
        self._position = value

    @property
    def energy(self):
        """Current energy (used by fast/special)."""
        return self._energy

    @energy.setter
    def energy(self, value):
        """Restricts energy from going below 0."""
        if value < 0:
            value = 0
        self._energy = value

    # --- Movements ---
    def fast(self, obs_loc):
        """
        Fast move:
        If energy >= 5: spend 5 energy, move (speed ± 1).
        If an obstacle is in the way, stop on it and crash.
        If energy is low, just move 1.
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
        Move at half speed ± 1 (no energy cost).
        Slow 'goes around' obstacles (no crash).
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
        """
        Special move:
        Subclasses decide the rules and message text.
        """
        pass

    def __str__(self):
        """Readable status for printing on each turn."""
        return self._name + " [Position - " + str(self.position + 1) + ", Energy - " + str(self.energy) + "]"
