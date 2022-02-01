from pynput.mouse import Listener, Button
from logging import basicConfig, info, DEBUG
from pyautogui import click
from threading import Thread

LOGFILE = 'C:/Users/sobra/OneDrive/Documentos/GitHub/Small_Personal_Projects/Python/CheckersMacro/mouse_log.log'
initial_position, final_position, initial_click = None, None, True

def makeMove():
    global initial_position, final_position
    info(f'First click at: {str(initial_position)}')
    info(f'Second click at: {str(final_position)}\n')
    click(initial_position[0], initial_position[1])
    click(final_position[0], final_position[1])
    initial_position, final_position = None, None

def getClickCoordinates(x, y, button, pressed):
    if not pressed: pass
    else:
        global initial_position, final_position, initial_click
        if button == Button.x2: initial_position, final_position = None, None   # front lateral mouse button
        if button == Button.middle: listener.stop()     # wheel mouse button
        if button == Button.left:
            if initial_click: initial_position = (x, y)
            else: final_position = (x, y)
            initial_click = not initial_click
    if initial_position is not None and final_position is not None: Thread(makeMove()).start()

if __name__ == '__main__':
    basicConfig(filename=LOGFILE, level=DEBUG, format='%(asctime)s: ')
    with Listener(on_click=getClickCoordinates) as listener: listener.join()