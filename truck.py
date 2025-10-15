from vehicle import Vehicle

class Truck(Vehicle):
    """A heavy truck that can ram through obstacles."""

    def special_move(self, obs_loc):
        if self.energy < 15:
            self.position = self.position + 1
            return self._name + " tries to ram forward, but is low on energy, moves 1 unit!"
        self.energy = self.energy - 15
        start = self.position
        move = 2 * self._speed
        end = start + move
        self.position = end
        return self._name + " rams forward " + str(end - start) + " units!"
