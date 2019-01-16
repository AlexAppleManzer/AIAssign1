from tkinter import *

root = Tk()
direction = Label(root, text="nice :)")
screen = Canvas(root, width=520, height=520)


class Dirt:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        dirtphoto = PhotoImage(file="dirt.gif")
        root.dirtphoto = dirtphoto
        self.data = screen.create_image((x * 50 + 15, y * 50 + 15), image=dirtphoto, anchor="nw")

    def get_loc(self):
        answer = (self.x, self.y)
        return answer

    def remove(self):
        screen.delete(self.data)


class VacuumCleaner:

    def __init__(self, x, y):
        p = PhotoImage(file="vacuum.gif")
        self.x = x
        self.y = y
        root.p = p
        self.vacuum = screen.create_image((x*50+10, y*50+10), image=p, anchor='nw')

    def go_up(self, f):
        if f.is_square(self.x, self.y - 1):
            direction.config(text="UP")
            screen.move(self.vacuum, 0, -50)
            self.y -= 1
            return 1
        else:
            return 0

    def go_down(self, f):
        if f.is_square(self.x, self.y + 1):
            direction.config(text="DOWN")
            screen.move(self.vacuum, 0, 50)
            self.y += 1
        else:
            return 0

    def go_left(self, f):
        if f.is_square(self.x - 1, self.y):
            direction.config(text="LEFT")
            screen.move(self.vacuum, -50, 0)
            self.x -= 1
            return 1
        else:
            return 0

    def go_right(self, f):
        if f.is_square(self.x + 1, self.y):
            direction.config(text="RIGHT")
            screen.move(self.vacuum, 50, 0)
            self.x += 1
        else:
            return 0

    def getpos(self):
        return [self.x, self.y]

    def vacuum_suck(self, f):
        direction.config(text="SUCK")
        f.make_clean(self.x, self.y)
        print("sucking at (%d, %d)..." % (self.x, self.y))


class Field:

    dirts = []
    squares = []
    dirtImages = []
    size = (0, 0)

    def __init__(self, x, y):
        self.dirts = [0] * x
        for i in range(x):
            self.dirts[i] = [0] * y

        self.squares = [0] * x
        for i in range(x):
            self.squares[i] = [0] * y

        self.size = (x, y)

    def is_dirt(self, x, y):
        return self.dirts[x][y]

    def make_dirty(self, x, y):
        self.dirts[x][y] = 1

    def make_clean(self, x, y):
        for i in range(len(self.dirtImages)):
            if self.dirtImages[i].get_loc() == (x, y):
                self.dirtImages[i].remove()

    def clean_up(self, x, y):
        screen.delete(self.dirtImages[self.dirts[x][y]])

    def is_square(self, x, y):
        return self.squares[x][y]

    def make_square(self, x, y):
        self.squares[x][y] = 1

    def remove_square(self, x, y):
        self.squares[x][y] = 0

    def draw(self):
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.squares[j][i]:
                    print("Drawing square at (%d, %d)..." % (j, i))
                    screen.create_rectangle((i*50 + 10, j*50 + 10), ((i+1)*50 + 10, (j+1)*50 + 10), fill='#000fff000')

                if self.dirts[j][i]:
                    print("Drawing dirt at (%d, %d)..." % (j, i))
                    self.dirtImages.append(Dirt(j, i))


def init_gui():

    direction.pack()
    screen.pack()

    botFrame = Frame(root, height=500, width=500)
    botFrame.pack(side=BOTTOM)

    f = Field(10, 10)
    f.make_square(5, 5)
    f.make_square(4, 5)
    f.make_square(5, 4)
    f.make_square(4, 4)

    f.make_dirty(4, 4)
    f.draw()
    v = VacuumCleaner(4, 4)

    up = Button(botFrame, text="UP", command=lambda: v.go_up(f))
    up.pack(side=LEFT)

    down = Button(botFrame, text="DOWN", command=lambda: v.go_down(f))
    down.pack(side=LEFT)

    left = Button(botFrame, text="LEFT", command=lambda: v.go_left(f))
    left.pack(side=LEFT)

    right = Button(botFrame, text="RIGHT", command=lambda: v.go_right(f))
    right.pack(side=LEFT)

    suck = Button(botFrame, text="SUCK", command=lambda: v.vacuum_suck(f))
    suck.pack(side=LEFT)


if __name__ == "__main__":
    init_gui()
    root.mainloop()

