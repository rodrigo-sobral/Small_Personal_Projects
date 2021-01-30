unique_symbols= { 1:'I', 5:'V', 10:'X', 50:'L', 100:'C', 500:'D', 1000:'M' }

def calculateRoman(integer, place):
    if integer==0: return ''
    elif 10-integer==1:
        pass
    #elif integer==1 or integer


def converter(integer):
    place=1
    roman=''
    while integer!=0:
        rest= integer%10
        integer//=10
        place+=1
        roman+=calculateRoman(rest, place)
    return roman

if __name__ == "__main__": 
    while True:
        try:
            integer = int(input('Insira um valor Inteiro: '))  
            if integer<1 or integer>4999: raise
            roman=converter(integer)
            #print("{} converts into {}".format(integer, roman))
            break
        except: pass
            