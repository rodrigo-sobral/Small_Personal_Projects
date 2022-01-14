from random import random
from tkinter import * 
from tkinter import messagebox
from turtle import *

window = Tk(className=' Make Your Bet') 
turtlescreen= None
SCREEN_WIDTH= 1420
SCREEN_HEIGHT= 720

GOAL_MARK_X= 550
GOAL_MARK_Y= 300
SQUARE_SIZE= 15
TURTLES_START_X= -450
TURTLES_START_Y= 250
MAX_TURTLE_SPEED= 25

turtle_selected= 0
turtles_colors= ["black", "green", "blue", "red", "orange", "brown", "grey", "purple", "pink", "dark blue", "dark green"]

def goTo(turtle, toX: int, toY: int):
    turtle.pu()
    turtle.goto(toX, toY)
    turtle.pd()

def drawSquare(goal_mark_turtle, size, color):
    goal_mark_turtle.begin_fill()
    goal_mark_turtle.fillcolor(color)
    for q in range(4):
        goal_mark_turtle.fd(size)
        goal_mark_turtle.left(90)
    goal_mark_turtle.end_fill()

def drawScene():
    bgcolor("grey")
    turtlescreen= Screen()
    turtlescreen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    turtlescreen.title('Turtles Race by Rodrigo Sobral')
    goal_mark_turtle= Turtle()
    goal_mark_turtle.speed(0)
    goal_mark_turtle.hideturtle()
    x= GOAL_MARK_X
    y= GOAL_MARK_Y

    goal_mark_turtle.pensize(1)
    goal_mark_turtle.pencolor("black")
    goal_mark_turtle._rotate(270)
    for i in range(40):
        goTo(goal_mark_turtle, x, y)
        if i<20: drawSquare(goal_mark_turtle, SQUARE_SIZE, 'black')
        else: drawSquare(goal_mark_turtle, SQUARE_SIZE, 'white')
        y-=SQUARE_SIZE
        goTo(goal_mark_turtle, x, y)
        if i<20: drawSquare(goal_mark_turtle, SQUARE_SIZE, 'white')
        else: drawSquare(goal_mark_turtle, SQUARE_SIZE, 'black')
        y-=SQUARE_SIZE
        if i==19:
            y=GOAL_MARK_Y
            x+=SQUARE_SIZE
    
def drawTurtles():
    y= TURTLES_START_Y
    turtles=[]
    for color in turtles_colors:
        runner_turtle= Turtle()
        runner_turtle.speed(0)
        goTo(runner_turtle, TURTLES_START_X, y)
        runner_turtle.shape('turtle')
        runner_turtle.pencolor(color)
        y-=40
        turtles.append(runner_turtle)
    return turtles

def startRace(turtles):
    while True:
        for runner in turtles:
            speed= random()*MAX_TURTLE_SPEED
            runner.fd(speed)
            if runner.xcor() >= GOAL_MARK_X-SQUARE_SIZE*2: return runner.pencolor()

def alertWinner(winner, turtle_selected):
    if winner==turtle_selected: messagebox.showinfo("Congratulations! Your {} Turtle won the race!")
    else: messagebox.showerror("")

def confirmBet(event):
    selection = event.widget.curselection()
    if selection:
        turtle_selected = event.widget.get(selection[0])
        confirmation = messagebox.askyesno(title='Confirmation', message='Do you want to confirm your bet in {} Turtle'.format(turtle_selected))
        if confirmation: 
            window.destroy()
            drawScene()
            turtles= drawTurtles()
            winner= startRace(turtles)
            turtlescreen.bye()
            alertWinner(winner, turtle_selected)

def makebet():
    window.geometry('500x230+350+250')
    yscrollbar = Scrollbar(window) 
    yscrollbar.pack(side = RIGHT, fill = Y) 
    bet_list = Listbox(window, selectmode='unique', yscrollcommand = yscrollbar.set) 
    bet_list.pack(padx = 10, pady = 10, expand = YES, fill = "both") 
    for color in range(len(turtles_colors)):
        bet_list.insert(END, turtles_colors[color]) 
        bet_list.itemconfig(color, bg = turtles_colors[color], fg='white') 
    bet_list.bind("<<ListboxSelect>>", confirmBet)
    window.mainloop() 


if __name__=="__main__":
    makebet()
 