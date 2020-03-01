from instructions import parseInstruction
import re
from memory import memory

class Program :
    def __init__(self) :
        self.labels = {}
        self.code = {}

    #file format:
    #.section .text
    #<code>
    #.section .strings
    #addr string
    #addr string
    #...
    def buildCode(self, lines) :
        state = 0
        for line in lines :
            l = line.strip()
            if (state == 0) :
                if (l == ".section .text") :
                    currAddr = memory.text[0]
                    state = 1
            elif (state == 1) :
                if (l == ".section .strings") :
                    currAddr = memory.strings[0]
                    state = 2
                else :                    
                    currAddr = self.addInstr(l, currAddr)
            elif (state == 2) :
                self.addString(l)

    def buildCodeFromFile(self, filename) :
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.buildCode(lines)

    def addInstr(self, l, addr) :
        #if it's a label, create an entry in the label dictionary, but don't bump the pointer
        if (l[-1] == ':') :
            #get label name:
            label = re.match(r'(.+):', l)[1]
            self.labels[label] = addr
            return addr
        else :
            #otherwise parse the instruction and add it to the list
            inst = parseInstruction(l)
            self.code[addr] = inst
            return addr + 4

    def addString(self, l) :
        match = re.match(r'(\S+) (.+)', l)
        addr = int(match[1])
        string = match[2]
        memory[addr] = string
                

### TEST ###
if __name__ == '__main__' :
    p = Program()
    p.buildCodeFromFile('testFile.asm')
    print(p.code)

    #bad test -- need to build machine simulator
    pc = 0
    while (pc in p.code) :
        print (p.code[pc])
        p.code[pc].exec()
        pc += 4