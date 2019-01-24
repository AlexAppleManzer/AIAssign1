from tkinter import *
from math import floor
from random import *
from Agent import Agent


class ScrollText:
    # class adapted from dev blog  https://knowpapa.com/scroll-text/'

    count = 1
    def __init__(self, frame):

        # add a frame and put a text area into it
        self.text = Text(frame, width=40)
        self.text.insert(END, "step\tcommand\t\tresult\tScore\n")

        # add a vertical scroll bar to the text area
        scroll = Scrollbar(frame)
        self.text.configure(yscrollcommand=scroll.set)

        # pack everything
        self.text.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)

    def write_text(self, text):
        # writes text to "console" to log what moves were made

        self.text.configure(state=NORMAL)
        self.text.insert(END, "%d\t" % self.count + text + "\n")
        self.text.configure(state=DISABLED)
        self.count += 1


class Square:

    def __init__(self, x, y, frame):
        # creates its "rectangle"
        self.frame = frame
        self.x = x
        self.y = y

        self.data = self.frame.create_rectangle((self.x * 50 + 10, self.y * 50 + 10), ((self.x + 1) * 50 + 10,
                                                (self.y + 1) * 50 + 10), fill='red')

    def make_activefill(self):
        # makes the square green when mouse is hovered over
        self.frame.itemconfig(self.data, activefill='green')

    def get_loc(self):
        # retrieves location of square
        answer = (self.x, self.y)
        return answer

    def change_color(self, color):
        # changes color of square
        self.frame.itemconfig(self.data, fill='%s' % color)

    def remove(self):
        # deletes self
        self.frame.delete(self.data)


class Dirt:

    def __init__(self, x, y, frame, dirtPics):
        self.frame = frame
        self.x = x
        self.y = y

        # creates image and adds to dirtPics library so the image doesn't get cleaned up
        self.dp = PhotoImage(file="dirt.gif")
        frame.dp = self.dp
        dirtPics.append(self.dp)

        # draws self on the screen
        self.data = self.frame.create_image((x * 50 + 15, y * 50 + 15), image=self.dp, anchor="nw", tags="image")

    def get_loc(self):
        # retrieves coordinates of self
        answer = (self.x, self.y)
        return answer

    def remove(self):
        # deletes self
        self.frame.delete(self.data)


class VacuumCleaner:

    def __init__(self, x, y, screen, direction, field):
        self.screen = screen

        # attaches image to screen so image doesn't get cleaned up
        p = PhotoImage(file="vacuum.gif")
        self.screen.p = p
        self.direction = direction
        self.x = x
        self.y = y
        self.field = field

        # draws vacuum
        self.vacuum = self.screen.create_image((x*50+10, y*50+10), image=p, anchor='nw')

    def go_up(self, log):
        # moves the vacuum up if there is a square available
        self.field.increment()
        if self.field.is_square(self.x, self.y - 1):
            # self.direction.config(text="UP")
            self.screen.move(self.vacuum, 0, -50)
            self.y -= 1
            log.write_text("Up\t\tTrue\t%d" % self.field.score)
            return 1
        else:
            log.write_text("Up\t\tFalse\t%d" % self.field.score)
            return 0

    def go_down(self, log):
        # moves the vacuum down if there is a square available
        self.field.increment()
        if self.field.is_square(self.x, self.y + 1):
            # self.direction.config(text="DOWN")
            self.screen.move(self.vacuum, 0, 50)
            self.y += 1
            log.write_text("Down\t\tTrue\t%d" % self.field.score)
            return 1
        else:
            log.write_text("Down\t\tFalse\t%d" % self.field.score)
            return 0

    def go_left(self, log):
        # moves the vacuum left if there is a square available
        self.field.increment()
        if self.field.is_square(self.x - 1, self.y):
            # self.direction.config(text="LEFT")
            self.screen.move(self.vacuum, -50, 0)
            self.x -= 1
            log.write_text("Left\t\tTrue\t%d" % self.field.score)
            return 1
        else:
            log.write_text("Left\t\tFalse\t%d" % self.field.score)
            return 0

    def go_right(self, log):
        # moves the vacuum right if there is a square available
        self.field.increment()
        if self.field.is_square(self.x + 1, self.y):
            # self.direction.config(text="RIGHT")
            self.screen.move(self.vacuum, 50, 0)
            self.x += 1
            log.write_text("Right\t\tTrue\t%d" % self.field.score)
            return 1
        else:
            log.write_text("Right\t\tFalse\t%d" % self.field.score)
            return 0

    def getpos(self):
        # retrieves position of vacuum
        return [self.x, self.y]

    def vacuum_suck(self, log):
        # sucks dirt if there is  dirt at the tile
        # self.direction.config(text="SUCK")
        self.field.increment()
        print("sucking at (%d, %d)..." % (self.x, self.y))
        if self.field.make_clean(self.x, self.y):
            log.write_text("Suck\t\tTrue\t%d" % self.field.score)
        else:
            log.write_text("Suck\t\tFalse\t%d" % self.field.score)


class Field:

    dirts = []
    squares = []
    dirtImages = []
    dirtPics = []
    size = (0, 0)

    def __init__(self, x, y, frame):
        self.frame = frame
        self.tracker = 0
        self.score = 0

        # creates empty 2 dimensional array to store dirt locations
        self.dirts = [0] * x
        for i in range(x):
            self.dirts[i] = [0] * y

        # creates empty 2 dimensional array to store squares
        self.squares = [0] * x
        for i in range(x):
            self.squares[i] = [0] * y

        self.size = (x, y)

    def is_dirt(self, x, y):
        # retrieves if there is a dirt at given location
        return self.dirts[x][y]

    def make_dirty(self, x, y):
        # makes the screen dirty at location
        self.dirts[x][y] = 1

    def mark_clean(self, x, y):
        # marks screen location as clean
        self.dirts[x][y] = 0

    def make_clean(self, x, y):
        # makes the screen clean at location
        for i in range(len(self.dirtImages)):
            if self.dirtImages[i].get_loc() == (x, y):
                self.dirtImages[i].remove()
                del self.dirtImages[i]
                return 1
        return 0

    def is_square(self, x, y):
        # checks if there is a square at location
        return self.squares[x][y]

    def make_square(self, x, y):
        # makes square at location
        self.squares[x][y] = 1

    def remove_square(self, x, y):
        # removes square at location
        self.squares[x][y] = 0

    def increment(self):
        self.tracker += 1
        if randint(0, 100) <= 10:
            for i in range(9999):
                x1 = floor(randint(0, self.size[0] - 1))
                y1 = floor(randint(0, self.size[1] - 1))
                if self.is_square(x1, y1):
                    print("adding dirt")
                    self.dirtImages.append(Dirt(x1, y1, self.frame, self.dirtPics))
                    break
        self.score += len(self.dirtImages)

    def draw(self):
        # draws screen with current data of rectangles and squares
        # loops through every possible tile in 10 x 10 area and checks for squares/dirts
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if self.squares[j][i]:
                    print("Drawing square at (%d, %d)..." % (j, i))
                    Square(j, i, self.frame)

                if self.dirts[j][i]:
                    print("Drawing dirt at (%d, %d)..." % (j, i))
                    self.dirtImages.append(Dirt(j, i, self.frame, self.dirtPics))


def init_gui():
    # initiates the window commands and sets up structure.
    root = Tk()
    screen = Canvas(root, width=520, height=520)
    direction = Label(root, text="Press Start to begin.")
    direction.grid(row=0, column=0)
    screen.grid(row=1, column=0)
    botFrame = Frame(root)
    botFrame.grid(row=2, column=0)
    field = Field(10, 10, screen)

    # start button initiates the setup process
    start = Button(botFrame, text="Start", command=lambda: place_squares(root, screen, direction, botFrame, start, field))
    start.pack()

    # keeps python from closing window
    root.mainloop()


def place_squares(root, screen, direction, botFrame, start, field):
    # initiates the gui to go to placement mode
    direction.config(text="Place Squares on Field")
    start.destroy()
    squares = []

    # draws all possible squares with activefill
    for i in range(field.size[1]):
        squares.append([])
        for j in range(field.size[0]):
            squares[i].append(Square(i, j, screen))
            squares[i][j].make_activefill()

    # on click event for signifying to make square at location
    def on_click(event):
        x = floor((event.x - 10) / 50)
        y = floor((event.y - 10) / 50)

        if not field.is_square(x, y):

            # marking square location in field object
            print("making square at", (x, y))
            field.make_square(x, y)

            # visual square color change
            squares[x][y].change_color('green')
        else:
            # unmarking square location at position
            print("deleting square at", (x, y))
            field.remove_square(x, y)

            # visual color revert
            squares[x][y].change_color('red')

    screen.bind("<Button-1>", on_click)

    # button defined for going to the next stage
    start = Button(botFrame, text="Start", command=lambda: place_dirts(root, screen, direction, botFrame,
                                                                       start, field, squares))
    start.pack()


def place_dirts(root, screen, direction, botFrame, start, field, squares):
    start.destroy()
    screen.delete("all")
    field.draw()
    direction.config(text="Place the initial dirt objects.")

    # local dirts array
    ds = []

    def on_click(event):
        # on click event for placing dirts
        x = floor((event.x - 10) / 50)
        y = floor((event.y - 10) / 50)
        if field.is_square(x, y):
            if not field.is_dirt(x, y):
                # visual change
                print("making dirt at", (x, y))
                ds.append(Dirt(x, y, screen, field.dirtPics))

                # marks location as dirty
                field.make_dirty(x, y)
            else:
                # visual change
                print("removing dirt at", (x, y))
                for i in range(len(ds)):
                    if ds[i].get_loc() == (x, y):
                        ds[i].remove()

                # marks location as clean
                field.mark_clean(x, y)

    screen.bind("<Button-1>", on_click)
    # button to initiate vacuum placement
    start = Button(botFrame, text="Start", command=lambda: place_vacuum(root, screen, direction,
                                                                        botFrame, start, field))
    start.pack()


def place_vacuum(root, screen, direction, botFrame, start, field):

    start.destroy()
    direction.config(text="Place the starting location for the vacuum")

    def on_click(event):
        # on click to place vacuum and then start the main phase of the program
        x = floor((event.x - 10) / 50)
        y = floor((event.y - 10) / 50)
        if field.is_square(x, y):
            print("placing Vacuum at", (x, y))

            screen.unbind("<Button-1>")
            init_field(root, screen, direction, botFrame, field, x, y)

    screen.bind("<Button-1>", on_click)


def init_field(root, screen, direction, botFrame, f, x, y):
    # creates vacuum cleaner and draws screen and then starts the game
    direction.config(text="Robot is going...")
    screen.unbind("<Button-1>")
    screen.delete("all")
    f.draw()
    v = VacuumCleaner(x, y, screen, direction, f)
    a = Agent()

    rightframe = Frame(root)
    log = ScrollText(rightframe)
    rightframe.grid(row=1, column=1)

    # buttons for manual control
    up = Button(botFrame, text="UP", command=lambda: v.go_up(log))
    up.pack(side=LEFT)

    down = Button(botFrame, text="DOWN", command=lambda: v.go_down(log))
    down.pack(side=LEFT)

    left = Button(botFrame, text="LEFT", command=lambda: v.go_left(log))
    left.pack(side=LEFT)

    right = Button(botFrame, text="RIGHT", command=lambda: v.go_right(log))
    right.pack(side=LEFT)

    suck = Button(botFrame, text="SUCK", command=lambda: v.vacuum_suck(log))
    suck.pack(side=LEFT)

    for i in range(1000):
        move = a.get_move(0)
        if move == 1:
            v.go_up(log)
        if move == 2:
            v.go_down(log)
        if move == 3:
            v.go_left(log)
        if move == 4:
            v.go_right(log)
        if move == 5:
            v.vacuum_suck(log)



if __name__ == "__main__":
    init_gui()


