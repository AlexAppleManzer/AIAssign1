from tkinter import *
from math import floor

class ScrollText:
    # class adapted from dev blog  https://knowpapa.com/scroll-text/'

    count = 0

    def __init__(self, frame):

        # add a frame and put a text area into it
        self.text = Text(frame, width=30)
        self.text.insert(END, "step\tcommand\t\tresult\n")

        # add a vertical scroll bar to the text area
        scroll = Scrollbar(frame)
        self.text.configure(yscrollcommand=scroll.set)

        # pack everything
        self.text.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)

    def write_text(self, text):
        self.text.configure(state=NORMAL)
        self.text.insert(END, "%d\t" % self.count + text + "\n")
        self.text.configure(state=DISABLED)
        self.count += 1


class Square:

    def __init__(self, x, y, frame):
        self.frame = frame
        self.x = x
        self.y = y

        self.data = self.frame.create_rectangle((self.x * 50 + 10, self.y * 50 + 10), ((self.x + 1) * 50 + 10,
                                                (self.y + 1) * 50 + 10), fill='red', activefill='green')
        print(self.data)

    def get_loc(self):
        answer = (self.x, self.y)
        return answer

    def change_color(self, color):
        self.frame.itemconfig(self.data, fill='%s' % color)

    def remove(self):
        self.frame.delete(self.data)


class Dirt:

    def __init__(self, x, y, frame):
        self.frame = frame
        self.x = x
        self.y = y

        dirtphoto = PhotoImage(file="dirt.gif")
        self.frame.dirtphoto = dirtphoto
        self.data = self.frame.create_image((x * 50 + 15, y * 50 + 15), image=dirtphoto, anchor="nw")

    def get_loc(self):
        answer = (self.x, self.y)
        return answer

    def remove(self):
        self.frame.delete(self.data)


class VacuumCleaner:

    def __init__(self, x, y, screen, direction, field):
        self.screen = screen
        p = PhotoImage(file="vacuum.gif")
        self.screen.p = p
        self.direction = direction
        self.x = x
        self.y = y
        self.field = field
        self.vacuum = self.screen.create_image((x*50+10, y*50+10), image=p, anchor='nw')

    def go_up(self):
        if self.field.is_square(self.x, self.y - 1):
            #self.direction.config(text="UP")
            self.screen.move(self.vacuum, 0, -50)
            self.y -= 1
            return 1
        else:
            return 0

    def go_down(self):
        if self.field.is_square(self.x, self.y + 1):
            #self.direction.config(text="DOWN")
            self.screen.move(self.vacuum, 0, 50)
            self.y += 1
            return 1
        else:
            return 0

    def go_left(self):
        if self.field.is_square(self.x - 1, self.y):
            #self.direction.config(text="LEFT")
            self.screen.move(self.vacuum, -50, 0)
            self.x -= 1
            return 1
        else:
            return 0

    def go_right(self):
        if self.field.is_square(self.x + 1, self.y):
            #self.direction.config(text="RIGHT")
            self.screen.move(self.vacuum, 50, 0)
            self.x += 1
            return 1
        else:
            return 0

    def getpos(self):
        return [self.x, self.y]

    def vacuum_suck(self):
        #self.direction.config(text="SUCK")
        self.field.make_clean(self.x, self.y)
        print("sucking at (%d, %d)..." % (self.x, self.y))


class Field:

    dirts = []
    squares = []
    dirtImages = []
    size = (0, 0)

    def __init__(self, x, y, frame):
        self.frame = frame

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
        self.frame.delete(self.dirtImages[self.dirts[x][y]])

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
                    Square(j, i, self.frame)

                if self.dirts[j][i]:
                    print("Drawing dirt at (%d, %d)..." % (j, i))
                    self.dirtImages.append(Dirt(j, i, self.frame))


def init_gui():

    root = Tk()
    screen = Canvas(root, width=520, height=520)
    direction = Label(root, text="Place Squares on Field")

    direction.grid(row=0, column=0)
    screen.grid(row=1, column=0)

    botFrame = Frame(root)
    botFrame.grid(row=2, column=0)

    field = Field(10, 10, screen)
    start = Button(botFrame, text="Start", command=lambda: place_squares(root, screen, direction, botFrame, start, field))
    start.pack()

    root.mainloop()


def place_squares(root, screen, direction, botFrame, start, field):
    start.destroy()
    squares = []
    for i in range(field.size[1]):
        squares.append([])
        for j in range(field.size[0]):
            squares[i].append(Square(i, j, screen))

    def on_click(event):
        print("clicked at", event.x, event.y)
        x = floor((event.x - 15) / 50)
        y = floor((event.y - 15) / 50)

        print("making square at", (x, y))
        field.make_square(x, y)
        print(squares[x][y].data)
        squares[x][y].change_color('green')


    screen.bind("<Button-1>", on_click)
    start = Button(botFrame, text="Start", command=lambda: init_field(root, screen, direction, botFrame, start, field))
    start.pack()


def init_field(root, screen, direction, botFrame, button, f):
    screen.delete("all")
    f.draw()
    v = VacuumCleaner(4, 4, screen, direction, f)

    rightframe = Frame(root)
    log = ScrollText(rightframe)
    rightframe.grid(row=1, column=1)

    up = Button(botFrame, text="UP", command=lambda: v.go_up())
    up.pack(side=LEFT)

    down = Button(botFrame, text="DOWN", command=lambda: v.go_down())
    down.pack(side=LEFT)

    left = Button(botFrame, text="LEFT", command=lambda: v.go_left())
    left.pack(side=LEFT)

    right = Button(botFrame, text="RIGHT", command=lambda: v.go_right())
    right.pack(side=LEFT)

    suck = Button(botFrame, text="SUCK", command=lambda: v.vacuum_suck())
    suck.pack(side=LEFT)


if __name__ == "__main__":
    init_gui()
