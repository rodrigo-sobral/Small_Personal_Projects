unique_symbols= { 'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000 }
spec_sym= ['I', 'X', 'C', 'M']

def calculateBuffer(buffer):
    result=0
    if len(buffer)==0: return 0
    for sym in enumerate(buffer):
        if result!=0 and sym[1] in spec_sym and unique_symbols[sym[1]]<result and buffer[sym[0]-1]!=buffer[sym[0]]: result-=unique_symbols[sym[1]]
        else: result+=unique_symbols[sym[1]]
    return result

def converter(roman):
    total= 0
    buffer=[]
    for sym in reversed(roman):
        #   kinda lexical analysis - it verifies if the symbols belong to the language
        if sym not in unique_symbols: return 0
        #   kinda syntax analysis - it verifies if the symbols are in the right order
        elif len(buffer)!=0 and sym not in spec_sym and unique_symbols[sym]<unique_symbols[buffer[len(buffer)-1]]: return 0
        else: buffer.append(sym)
    return total+calculateBuffer(buffer)

if __name__ == "__main__":   
    roman= "XCXC"
    integer=converter(roman)
    if integer==0: print("Error, you inserted a wrong numeration!")
    else: print("{} converts into {}".format(roman, integer))