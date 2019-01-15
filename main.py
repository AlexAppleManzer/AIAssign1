from tkinter import *

root = Tk()
direction = Label(root, text="nice :)")
screen = Canvas(root, width=520, height=520)

class VacuumCleaner:

    p = 0
    vacuum = 0

    def __init__(self, x, y):
        print("hello")
        p = PhotoImage(file="vacuum.gif")
        root.p = p
        self.vacuum = screen.create_image((x*50+10, y*50+10), image=p, anchor='nw')

    def go_up(self):
        direction.config(text="UP")
        screen.move(self.vacuum, 0, -50)

    def go_down(self):
        direction.config(text="DOWN")
        screen.move(self.vacuum, 0, 50)

    def go_left(self):
        direction.config(text="LEFT")
        screen.move(self.vacuum, -50, 0)

    def go_right(self):
        direction.config(text="RIGHT")
        screen.move(self.vacuum, 50, 0)



class field:

    dirts = []
    squares = []
    size = (0, 0)

    def __init__(self, x, y):
        self.dirts = [0] * x
        for i in range(x):
            self.dirts[i] = [0] * y

        self.squares = [0] * x
        for i in range(x):
            self.squares[i] = [0] * y

        self.size = (x, y)

    def make_dirty(self, x, y):
        self.dirts[x][y] = 1

    def make_clean(self, x, y):
        self.dirts[x][y] = 0

    def make_square(self, x, y):
        self.squares[x][y] = 1

    def remove_square(self, x, y):
        self.squares[x][y] = 0

    def draw(self):
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.squares[j][i]:
                    print("Drawing (%d, %d)..." % (j, i))
                    screen.create_rectangle((i*50 + 10, j*50 + 10), ((i+1)*50 + 10, (j+1)*50 + 10), fill='#000fff000')


def get_coords(x, y):
    return[x*50+25, y*50 + 25]





def vacuum_suck():
    direction.config(text="SUCK")


def init_gui():

    direction.pack()
    screen.pack()

    botFrame = Frame(root, height=500, width=500)
    botFrame.pack(side=BOTTOM)

    f = field(10, 10)
    f.make_square(5, 5)
    f.draw()
    v = VacuumCleaner(0, 0)

    up = Button(botFrame, text="UP", command=v.go_up)
    up.pack(side=LEFT)

    down = Button(botFrame, text="DOWN", command=v.go_down)
    down.pack(side=LEFT)

    left = Button(botFrame, text="LEFT", command=v.go_left)
    left.pack(side=LEFT)

    right = Button(botFrame, text="RIGHT", command=v.go_right)
    right.pack(side=LEFT)

    suck = Button(botFrame, text="SUCK", command=vacuum_suck)
    suck.pack(side=LEFT)


if __name__ == "__main__":
    init_gui()
    root.mainloop()

