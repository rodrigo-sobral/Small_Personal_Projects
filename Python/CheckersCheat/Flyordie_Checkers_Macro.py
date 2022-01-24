from pynput.mouse import Listener, Button, Controller
import pyautogui

mouse_controller = Controller()
initial_position, final_position = None, None

def makeMove():
    global initial_position, final_position
    pyautogui.moveTo(initial_position[0], initial_position[1])
    print ("Inital position: " + str(initial_position))
    pyautogui.moveTo(final_position[0], final_position[1])
    print ("Final position: " + str(final_position))

def getClickCoordinates(x, y, button, pressed):
    global initial_position, final_position
    if pressed and button == Button.x2: initial_position, final_position = None, None   # front lateral mouse button
    if button==Button.left:
        if pressed: initial_position, final_position = (x, y), None
        else: final_position = (x, y)
    if initial_position and final_position: makeMove()

with Listener(on_click=getClickCoordinates) as listener: listener.join()
