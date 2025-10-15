import random
from vehicle import Vehicle

class Motorcycle(Vehicle):
    """A motorcycle with a Wheelie special move; has a better slow speed."""

    def slow(self, obs_loc):
        """
        Motorcycle slow:
          - 0.75×speed ± 1, no energy cost
          - Does not crash on obstacles (go around)
          - If an obstacle is in the path, say 'slowly dodges the obstacle'
        """
        base = int(0.75 * self._speed)
        move = base + random.randint(-1, 1)
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


    def special_move(self, obs_loc):
        if self.energy < 15:
            self.position = self.position + 1
            return self._name + " attempts a wheelie but is low on energy, moves 1 unit!"

        self.energy = self.energy - 15
        roll = random.random()
        if roll < 0.75:
            move = 2 * self._speed + random.randint(-1, 1)
            if move < 0:
                move = 0
            start = self.position
            end = start + move
            if obs_loc is not None and start < obs_loc <= end:
                self.position = obs_loc
                return self._name + " pops a wheelie and CRASHES!"
            self.position = end
            return self._name + " pops a wheelie and moves " + str(end - start) + " units!!"
        else:
            self.position = self.position + 1
            return self._name + " tries a wheelie and falls—moves 1 unit!"
