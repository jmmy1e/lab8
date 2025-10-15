import random
from vehicle import Vehicle

class Car(Vehicle):
    """A car with a Nitro Boost special move."""

    def special_move(self, obs_loc):
        """
        Car's special:
        Nitro Boost: 1.5× speed ±1 (costs 15 energy).
        If there’s an obstacle in the path, the car crashes on it.
        If energy is low, just move 1.
        """
        if self.energy < 15:
            self.position = self.position + 1
            return self._name + " tries nitro boost but is low on energy, moves 1 unit!"

        self.energy = self.energy - 15
        move = int(1.5 * self._speed) + random.randint(-1, 1)
        if move < 0:
            move = 0

        start = self.position
        end = start + move

        if obs_loc is not None and start < obs_loc <= end:
            self.position = obs_loc
            return self._name + " uses nitro boost and CRASHES!"
        else:
            self.position = end
            return self._name + " uses nitro boost and moves " + str(end - start) + " units!"
