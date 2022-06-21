def command_help() -> None:
    print('Available commands:')
    print('\t-h\t\tPrint this help')
    print('\t--email\t\tEmail address to send the log to')
    print('\t--addr\t\tIP address to connect to')
    print('\t--port\t\tPort to connect to (default is 4444)')
    print('\t--limit\t\tMaximum number of characters to send per email (default is 50)')
    print('\t-k\t\tConsiders only keyobard inputs (by default considers all inputs)')
    print('\t-m\t\tConsiders only mouse inputs (by default it considers all inputs)')
    print()
    exit(1)
    

def triggerArgumentsError() -> None:
    print('Wrong command line arguments. Check help menu.')
    command_help()
    exit(1)

def triggerEmailError(errortype: str) -> None:
    if errortype == 'login':
        print('Something went wrong during authentication, verify your credentials or your internet access.')
    exit(1)
