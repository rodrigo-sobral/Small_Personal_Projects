from pynput.mouse import Listener, Button, Controller
from time import sleep

mouse_controller = Controller()
initial_position, final_position = None, None

def makeMove(initial_position, final_position):
    sleep(0.5)
    if initial_position and final_position:
        print ("Current position: " + str(mouse_controller.position))
        mouse_controller.move(initial_position[0], initial_position[1])
        print ("Current position: " + str(mouse_controller.position))
        mouse_controller.press(Button.left)
        mouse_controller.move(final_position[0]-initial_position[0], final_position[1]-initial_position[1])
        print ("Current position: " + str(mouse_controller.position))
        mouse_controller.release(Button.left)

def getClickCoordinates(x, y, button, pressed):
    global initial_position, final_position
    if pressed and button == Button.x2: initial_position, final_position = None, None
    if button==Button.left:
        if pressed: initial_position = (x, y)
        else: final_position = (x, y)
    makeMove(initial_position, final_position)

with Listener(on_click=getClickCoordinates) as listener: listener.join()
