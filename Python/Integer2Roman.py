unique_symbols= { 1:'I', 5:'V', 10:'X', 50:'L', 100:'C', 500:'D', 1000:'M' }

def calculateRoman(algarism, place):
    if algarism==0: return ''
    elif place>=4: return algarism * unique_symbols[1000]
    elif algarism>5:
        if algarism==9: return unique_symbols[10**(place-1)]+unique_symbols[10**place]
        else: return unique_symbols[5*10**(place-1)] + (algarism-5) * unique_symbols[10**(place-1)]
    elif algarism<5:
        if algarism==4: return unique_symbols[10**(place-1)] + unique_symbols[5*10**(place-1)]
        else: return algarism * unique_symbols[10**(place-1)]
    else: return unique_symbols[5*10**(place-1)]

def converter(integer):
    place=0
    roman=''
    while integer!=0:
        rest= integer%10
        integer//=10
        place+=1
        roman= calculateRoman(rest, place) + roman
    return roman

if __name__ == "__main__": 
    while True:
        try:
            integer = input('Insert an Integer: ')
            if integer.isdecimal(): integer= int(integer)
            else: 
                print('Insert a valid Integer')
                continue
            if integer<1 or integer>10000: raise
            roman=converter(integer)
            print("{} converts into {}".format(integer, roman))
            break
        except: print("Integer is too high")