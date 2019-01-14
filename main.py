from tkinter import *

root = Tk()
direction = Label(root, text="nice :)")

direction.pack()

screen = Canvas(root, width=500, height=500)
screen.pack()


def go_up():
    direction.config(text="UP")


def go_down():
    direction.config(text="DOWN")


def go_left():
    direction.config(text="LEFT")


def go_right():
    direction.config(text="RIGHT")


def suck():
    direction.config(text="SUCK")


botFrame = Frame(root, height=500, width=500)
botFrame.pack(side=BOTTOM)

up = Button(botFrame, text="UP", command=go_up)
up.pack(side=LEFT)

down = Button(botFrame, text="DOWN", command=go_down)
down.pack(side=LEFT)

left = Button(botFrame, text="LEFT", command=go_left)
left.pack(side=LEFT)

right = Button(botFrame, text="RIGHT", command=go_right)
right.pack(side=LEFT)

suck = Button(botFrame, text="SUCK", command=suck)
suck.pack(side=LEFT)

p = PhotoImage(file="Vaccum.gif")

screen.create_image((250, 250), image=p, anchor='center')

root.mainloop()
