
class Agent:
    idle = 0
    up = 1
    down = 2
    left = 3
    right = 4
    suck = 5

    def __init__(self, x, y, s):
        # initiates agent
        self.x = x
        self.y = y
        self.sensor = False
        self.last_move = 0
        self.squares = s

        print("agent generated")

    def get_move(self, is_dirt):

        def can_move(dir):
            if dir == self.up:
                return self.squares[self.x][self.y - 1]

            if dir == self.down:
                return self.squares[self.x][self.y + 1]

            if dir == self.left:
                return self.squares[self.x - 1][self.y]

            if dir == self.right:
                return self.squares[self.x + 1][self.y]

            return 0

        if is_dirt:
            self.last_move = 5
            return self.suck
        else:
            option = [0, 9999]

            for i in range(1, 5):
                print(can_move(i))
                if option[1] > can_move(i) > 0:
                    option = [i, can_move(i)]

            if option[0] == self.up:
                self.y -= 1
                self.squares[self.x][self.y] += 1
                print("current location: %d, %d" % (self.x, self.y))
            if option[0] == self.down:
                self.y += 1
                self.squares[self.x][self.y] += 1
                print("current location: %d, %d" % (self.x, self.y))
            if option[0] == self.left:
                self.x -= 1
                self.squares[self.x][self.y] += 1
                print("current location: %d, %d" % (self.x, self.y))
            if option[0] == self.right:
                self.x += 1
                self.squares[self.x][self.y] += 1
                print("current location: %d, %d" % (self.x, self.y))

            return option[0]

    def sense(self, sensor):
        self.sensor = sensor
