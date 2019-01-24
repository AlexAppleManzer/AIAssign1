
class Agent:
    up = 1
    down = 2
    left = 3
    right = 4
    suck = 5

    def __init__(self, x, y):
        # initiates agent
        self.location = (x, y)
        self.sensor = False
        self.last_move = 0
        print("agent generated")

    def get_move(self, is_dirt):
        if is_dirt:
            self.last_move = 5
            return self.suck

        return self.right

    def sense(self, sensor):
        self.sensor = sensor
