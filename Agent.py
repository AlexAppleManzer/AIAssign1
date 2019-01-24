
class Agent:
    up = 1
    down = 2
    left = 3
    right = 4
    suck = 5

    def __init__(self):
        # initiates agent
        print("agent generated")

    def get_move(self, is_dirt):
        if is_dirt:
            return self.suck

        return self.right
