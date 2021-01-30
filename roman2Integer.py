unique_symbols= { 'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000 }
spec_sym= ['I', 'X', 'C', 'M']

def calculateBuffer(buffer):
    result=0
    if len(buffer)==0: return 0
    for sym in enumerate(buffer):
        #   ensures we dont have things like VX
        if sym[1] not in spec_sym and unique_symbols[sym[1]]<result and buffer[sym[0]-1]!=buffer[sym[0]]: return 0
        #   it calculates thins like IV - 5-1
        elif result!=0 and sym[1] in spec_sym and unique_symbols[sym[1]]<result and buffer[sym[0]-1]!=buffer[sym[0]]: result-=unique_symbols[sym[1]]
        #   it calculates thins like VI - 5+1
        else: result+=unique_symbols[sym[1]]
    return result

def converter(roman):
    buffer=[]
    for sym in reversed(roman):
        #   kinda lexical analysis - it verifies if the symbols belong to the language
        if sym not in unique_symbols: return 0
        #   kinda syntax analysis - it verifies if the symbols are in the right order
        #   it tests if we have XIXI e.g.
        elif len(buffer)>1 and unique_symbols[sym]<=unique_symbols[buffer[-2]] and unique_symbols[sym]<unique_symbols[buffer[-1]]: return 0
        #   it tests if we have IIII e.g.
        elif len(buffer)>2 and sym!='M' and sym==buffer[-1] and sym==buffer[-2] and sym==buffer[-3]: return 0
        else: buffer.append(sym)
    return calculateBuffer(buffer)

if __name__ == "__main__": 
    while True:
        roman = str(input('Insert a Roman value: '))  
        integer=converter(roman)
        if integer!=0: 
            print("{} converts into {}".format(roman, integer))
            break
        else:
            print(chr(27) + "[2J")
            print("Error, you inserted a wrong numeration!")