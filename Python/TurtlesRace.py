from random import random
from tkinter import * 
import turtle

n_min=1
n_max=10
v_max=25
chegou=400

def drawScene():
    turtle.bgcolor("grey")
    meta= turtle.Turtle()
    meta.speed(0)
    x=chegou
    y=265
    lado_quadrado=15
    def quadrado_preto(meta):
        meta.begin_fill()
        meta.fillcolor("black")
        for q in range(4):
            meta.fd(lado_quadrado)
            meta.left(90)
        meta.end_fill()
    def quadrado_branco(meta):
        meta.begin_fill()
        meta.fillcolor("white")
        for q in range(4):
            meta.fd(lado_quadrado)
            meta.left(90)
        meta.end_fill()    

    #DESENHAR META--------------------
    meta.pensize(1)
    meta.pencolor("black")
    meta._rotate(270)
    for j in range(20):
        meta.pu()
        meta.goto(x,y)
        meta.pd()
        quadrado_preto(meta)
        y-=lado_quadrado
        meta.pu()
        meta.goto(x,y)
        meta.pd()
        quadrado_branco(meta)
        y-=lado_quadrado
    y=265
    x+=lado_quadrado
    for j in range(20):
        meta.pu()
        meta.goto(x,y)
        meta.pd()
        quadrado_branco(meta)
        y-=lado_quadrado
        meta.pu()
        meta.goto(x,y)
        meta.pd()
        quadrado_preto(meta)
        y-=lado_quadrado
    meta.hideturtle()

def drawTurtles(cavalos, MAX_CAVALOS):
    x=-550
    y=200
    for i in range(MAX_CAVALOS):
        cavalos[i].pu()
        cavalos[i].goto(x,y)
        cavalos[i].pd()
        cavalos[i].speed(0)
        y-=40
        
def correr(cavalos, MAX_CAVALOS, cores):
    while True: 
        aposta= int(input("Em que cavalo irá apostar? => "))
        if (aposta<=MAX_CAVALOS and aposta>0): break
    print("\n\tGO!!!\n")
    while True:
        velocidade= v_max*random()
        cavalos[0].fd(velocidade)
        if (cavalos[0].xcor()>=chegou):
            vencedor=0
            break
        velocidade= v_max*random()
        cavalos[1].fd(velocidade)
        if (cavalos[1].xcor()>=chegou):
            vencedor=1
            break
        velocidade= v_max*random()
        cavalos[2].fd(velocidade)
        if (cavalos[2].xcor()>=chegou):
            vencedor=2
            break
        velocidade= v_max*random()
        cavalos[3].fd(velocidade)
        if (cavalos[3].xcor()>=chegou):
            vencedor=3
            break
        velocidade= v_max*random()
        cavalos[4].fd(velocidade)
        if (cavalos[4].xcor()>=chegou):
            vencedor=4
            break
        velocidade= v_max*random()
        cavalos[5].fd(velocidade)
        if (cavalos[5].xcor()>=chegou):
            vencedor=5
            break
        velocidade= v_max*random()
        cavalos[6].fd(velocidade)
        if (cavalos[6].xcor()>=chegou):
            vencedor=6
            break
        velocidade= v_max*random()
        cavalos[7].fd(velocidade)
        if (cavalos[7].xcor()>=chegou):
            vencedor=7
            break
        velocidade= v_max*random()
        cavalos[8].fd(velocidade)
        if (cavalos[8].xcor()>=chegou):
            vencedor=8
            break
        velocidade= v_max*random()
        cavalos[9].fd(velocidade)
        if (cavalos[9].xcor()>=chegou):
            vencedor=9
            break
        velocidade= v_max*random()
        cavalos[10].fd(velocidade)
        if (cavalos[10].xcor()>=chegou):
            vencedor=10
            break
        
    if (vencedor+1==aposta):
        print("PARABÉNS!!! O CAVALO EM QUE APOSTOU GANHOU A CORRIDA!!!\n\n")
    else:
        print("PERDEU A SUA APOSTA!!! O CAVALO VENCEDOR FOI O CAVALO", cores[vencedor],"!!!\n\n")

def makebet():
    bet=0
    turtles=["black", "green", "blue", "red", "orange", "brown", "yellow", "purple", "pink", "dark blue", "dark green"]
    window = Tk() 
    yscrollbar = Scrollbar(window) 
    yscrollbar.pack(side = RIGHT, fill = Y) 
    bet_list = Listbox(window, selectmode='unique', yscrollcommand = yscrollbar.set) 
    bet_list.pack(padx = 10, pady = 10, expand = YES, fill = "both") 
    for each_item in range(len(turtles)):
        bet_list.insert(END, turtles[each_item]) 
        bet_list.itemconfig(each_item, bg = "light grey" if each_item % 2 == 0 else "white") 
    window.mainloop() 


if __name__=="__main__":
    #drawScene()
    #drawTurtles()
    makebet()

  