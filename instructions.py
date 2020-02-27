from registers import registerFile
import re

#base class for instructions
class Instruction :
    def __init__(self, opcode) :
        self.opcode = opcode #name of opcode
        self.src1 = None #ref to src1 register
        self.src2 = None #ref to src2 register
        self.dst = None #ref to destination register
        self.imm = None #immediate value (if needed)
        self.addr = None #label to jump to or label name

    #execute the instruction, including updating memory/registers as necessary
    #assumption: exec does not check dependences. This will be checked at other phases in the code
    #could simply schedule code for execution, rather than directly executing it
    #TODO: extend these to handle different timing models -- move the basic exec code into a "simpleExec" function instead
    def exec(self) :
        raise NotImplementedError('exec not implemented for ' + self.opcode)

#base class for u-type instructions
class UInstruction(Instruction) :
    def __init__(self, dst, imm, opcode) :
        super().__init__(opcode)
        self.dst = dst
        self.imm = imm

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.imm)

#base class for r-type instructions
class RInstruction(Instruction) :

    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\w+) (\w+), (\w+), (\w+)', instr)
        return cls(match[3], match[4], match[2], match[1])

    def __init__(self, src1, src2, dst, opcode) :
        super().__init__(opcode)
        self.src1 = src1
        self.src2 = src2
        self.dst = dst

    def exec(self) :
        s1 = registerFile[self.src1].read()
        s2 = registerFile[self.src2].read()
        d = self.funcExec(s1, s2)
        registerFile[self.dst].write(d)

    def funcExec(self, s1, s2) :
        raise NotImplementedError("funcExec not implemented for r-type instruction " + self.opcode)

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.src1 + " " + self.src2)

#base class for i-type instructions
class IInstruction(Instruction) :
    def __init__(self, src1, imm, dst, opcode) :
        super().__init__(opcode)
        self.src1 = src1
        self.imm = imm
        self.dst = dst

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.src1 + " " + self.imm)

###### Instructions ######

opCodeMap = {}

def concreteInstruction(cls) :
    cls._instInit()
    return cls

@concreteInstruction
class AddInstruction(RInstruction) :
    def funcExec(self, s1, s2) :
        return s1 + s2

    @classmethod
    def _instInit(cls) :
        opCodeMap['ADD'] = cls

@concreteInstruction
class SubInstruction(RInstruction) :
    def funcExec(self, s1, s2) :
        return s1 - s2

    @classmethod
    def _instInit(cls) :
        opCodeMap['SUB'] = cls        

@concreteInstruction
class MulInstruction(RInstruction) :
    def funcExec(self, s1, s2) :
        return s1 * s2

    @classmethod
    def _instInit(cls) :
        opCodeMap['MUL'] = cls        

@concreteInstruction
class DivInstruction(RInstruction) :
    def funcExec(self, s1, s2) :
        return s1 // s2      

    @classmethod
    def _instInit(cls) :
        opCodeMap['DIV'] = cls        

###### Parsing ######

#Parse the instruction and generate the right derived instruction from it
#The instruction is a single instruction string
def parseInstruction(inst) :
    base = inst.strip()
    opcode = re.match(r'(\w+)', base)[0]
    return opCodeMap[opcode].parse(base)

####### Test #######

def testAdd() :
    registerFile['t0'].write(3)
    registerFile['t1'].write(4)
    print(registerFile['t2'])
    # inst1 = AddInstruction(src1 = 't0', src2 = 't1', dst = 't2', opcode = 'ADD')
    inst1 = parseInstruction("ADD t2, t0, t1")
    print(inst1)
    inst1.exec()
    print(registerFile['t2'])

def testParse() :
    inst = parseInstruction("  ADD t2, t0, t1 ")
    print(inst)

def testExecList() :
    registerFile['t0'].write(3)
    registerFile['t1'].write(4)
    registerFile['t2'].write(5)
    registerFile['t3'].write(6)
    insts = [
        'ADD t4, t0, t1',
        'ADD t5, t2, t3',
        'MUL t6, t4, t5'
    ]
    ops = [parseInstruction(i) for i in insts]
    for o in ops :
        o.exec()

    print(registerFile['t4'])
    print(registerFile['t5'])
    print(registerFile['t6'])

if __name__ == '__main__' :
    testExecList()
