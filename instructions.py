from registers import registerFile
from memory import memory
import re

#base class for instructions
class Instruction :
    def __init__(self, opcode) :
        self.opcode = opcode #name of opcode

    #execute the instruction, including updating memory/registers as necessary
    #assumption: exec does not check dependences. This will be checked at other phases in the code
    #could simply schedule code for execution, rather than directly executing it
    #TODO: extend these to handle different timing models -- move the basic exec code into a "simpleExec" function instead
    def exec(self) :
        raise NotImplementedError('exec not implemented for ' + self.opcode)

#base class for u-type instructions
class UInstruction(Instruction) :

    @classmethod
    def parse(cls, instr) :
        print(instr)
        match = re.match(r'(\S+) (\S+), (\S+)', instr)
        return cls(match[2], match[3], match[1])

    def __init__(self, dst, imm, opcode) :
        super().__init__(opcode)
        self.dst = dst
        self._imm = 0
        self.imm = imm

    @property
    def dsttype(self) :
        raise NotImplementedError("Define type in derived class")

    @property
    def imm(self) :
        return self._imm

    @imm.setter
    def imm(self, value) :
        raise NotImplementedError("Define immediate setter in derived class")

    def exec(self) :
        destReg = registerFile[self.dst]
        assert destReg.type == self.dsttype, "Destination register is not " + str(self.dsttype)

        d = self.funcExec(self.imm)

        destReg.write(d)

    def funcExec(self, imm) :
        raise NotImplementedError("funcExec not implemented for u-type instruction " + self.opcode)

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + str(self.imm))

#base class for u-type instruction with integer immediate
class IUInstruction(UInstruction) :
    @property
    def dsttype(self) :
        return int

    @UInstruction.imm.setter # pylint: disable=no-member
    def imm(self, value) :
        new_imm = int(value)
        assert (new_imm < (2 ** 20)), "Immediate must be less than 2^20"
        self._imm = new_imm

#base class for u-type instruction with float immediate
class FUInstruction(UInstruction) :
    @property
    def dsttype(self) :
        return float

    @UInstruction.imm.setter # pylint: disable=no-member
    def imm(self, value) :
        new_imm = float(value)
        self._imm = new_imm

#base class for 2-operand r-type instructions
class ORInstruction(Instruction) :
    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\S+) (\S+), (\S+)', instr)
        return cls(match[3], match[2], match[1])

    def __init__(self, src1, dst, opcode) :
        super().__init__(opcode)
        self.src1 = src1
        self.dst = dst

    @property 
    def srctype(self) :
        raise NotImplementedError("Define type in the derived class!")

    @property
    def dsttype(self) :
        raise NotImplementedError("Define type in the derived class!")

    def exec(self) :
        src1reg = registerFile[self.src1]
        assert src1reg.type == self.srctype, "Src 1 register is not " + str(self.srctype)
        s1 = src1reg.read()

        d = self.funcExec(s1)

        destReg = registerFile[self.dst]    
        assert destReg.type == self.dsttype, "Destination register is not " + str(self.dsttype)

        destReg.write(d)

    def funcExec(self, s1) :
        raise NotImplementedError("funcExec not implemented for 2-operand r-type instruction " + self.opcode)

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.src1)    

#base class for integer 2-operand instructions
class IORInstruction(ORInstruction) :
    @property
    def srctype(self) :
        return int

    @property
    def dsttype(self) :
        return int

#base class for fp 2-operand instructions
class FORInstruction(ORInstruction) :
    @property
    def srctype(self) :
        return float

    @property
    def dsttype(self) :
        return float             

#base class for 3-operand r-type instructions
class RInstruction(Instruction) :

    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\S+) (\S+), (\S+), (\S+)', instr)
        return cls(match[3], match[4], match[2], match[1])

    def __init__(self, src1, src2, dst, opcode) :
        super().__init__(opcode)
        self.src1 = src1
        self.src2 = src2
        self.dst = dst

    @property 
    def srctype(self) :
        raise NotImplementedError("Define type in the derived class!")

    @property
    def dsttype(self) :
        raise NotImplementedError("Define type in the derived class!")

    def exec(self) :
        src1reg = registerFile[self.src1]
        assert src1reg.type == self.srctype, "Src 1 register is not " + str(self.srctype)
        s1 = src1reg.read()

        src2reg = registerFile[self.src2]
        assert src2reg.type == self.srctype, "Src 2 register is not " + str(self.srctype)
        s2 = src2reg.read()

        d = self.funcExec(s1, s2)

        destReg = registerFile[self.dst]    
        assert destReg.type == self.dsttype, "Destination register is not " + str(self.dsttype)

        destReg.write(d)

    def funcExec(self, s1, s2) :
        raise NotImplementedError("funcExec not implemented for r-type instruction " + self.opcode)

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.src1 + " " + self.src2)

#base class for int r-type instructions
class IRInstruction(RInstruction) :
    @property
    def srctype(self) :
        return int

    @property
    def dsttype(self) :
        return int


#base class for fp r-type instructions
class FRInstruction(RInstruction) :
    @property
    def srctype(self) :
        return float

    @property
    def dsttype(self) :
        return float

#base class for fp comparison instructions
class FCmpInstruction(RInstruction) :
    @property
    def srctype(self) :
        return float

    @property
    def dsttype(self) :
        return int

#base class for i-type instructions
class IInstruction(Instruction) :

    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\S+) (\S+), (\S+), (\S+)', instr)
        return cls(match[3], match[4], match[2], match[1])
        
    def __init__(self, src1, imm, dst, opcode) :
        super().__init__(opcode)
        self.src1 = src1
        self.imm = imm
        self.dst = dst

    def exec(self) :
        src1reg = registerFile[self.src1]
        assert src1reg.type == int, "Src 1 register is not an integer"
        s1 = src1reg.read()

        #cast imm to the type of the destination register
        destReg = registerFile[self.dst]    
        assert destReg.type == int, "Destination register is not an integer"
    
        imm = destReg.type(self.imm)
        assert (imm < (2 ** 12)), "Immediate value is too large; must fit in 12 bits"

        d = self.funcExec(s1, imm)
        destReg.write(d)

    def funcExec(self, s1, imm) :
        raise NotImplementedError("funcExec not implemented for i-type instruction " + self.opcode)

    def __str__(self) :
        return str(self.opcode + " " + self.dst + " " + self.src1 + " " + self.imm)

#base class for memory instruction
class MemInstruction(Instruction) :

    #LOAD: LW reg1, imm(reg2) : reg1 = *(reg2 + imm)
    #STORE: SW reg1, imm(reg2) : *(reg2 + imm) = reg1

    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\S+) (\S+), (\S+)\((\S+)\)', instr)
        return cls(match[2], match[4], match[3], match[1])
        
    def __init__(self, reg1, reg2, imm, opcode) :
        super().__init__(opcode)
        self.reg1 = reg1
        self.reg2 = reg2
        self.imm = imm

    def _calculateAddress(self) :
        offset = int(self.imm)
        assert (offset < 2 ** 12), "Offset too large"

        base = registerFile[self.reg2].read()

        return base + offset

    def __str__(self) :
        return str(self.opcode + " " + self.reg2 + " " + self.imm + "(" + self.reg1 + ")")
    
#base class for int/fp loads
class LDInstruction(MemInstruction) :

    def exec(self) :
        #calculate address
        addr = self._calculateAddress()

        #perform load
        val = self.funcExec(addr)

        #store result into register
        assert(type(val) == self.dsttype), "Value in memory not of type " + str(self.dsttype)

        destReg = registerFile[self.reg1]

        assert (destReg.type == self.dsttype), "Destination register not of type " + str(self.dsttype)

        destReg.write(val)

    def funcExec(self, addr) :
        return memory[addr]

    @property
    def dsttype(self) :
        raise NotImplementedError("Specialize type in derived class")

#base class for int/fp stores
class STInstruction(MemInstruction) :

    def exec(self) :
        #calculate address
        addr = self._calculateAddress()

        #get value from register
        srcReg = registerFile[self.reg1]

        assert (srcReg.type == self.srctype), "Source register not of type " + str(self.srctype)

        val = srcReg.read()

        #perform store
        self.funcExec(addr, val)

    def funcExec(self, addr, val) :
        print("updating memory location: " + hex(addr))
        memory[addr] = val

    @property
    def srctype(self) :
        raise NotImplementedError("Specialize type in derived class")

#base class for IO magic instructions
class IOInstruction(Instruction) :

    @classmethod
    def parse(cls, instr) :
        match = re.match(r'(\S+) (\S+)', instr)
        return cls(match[2], match[1])

    def __init__(self, reg, opcode) :
        super().__init__(opcode)
        self.reg = reg

    def __str__(self) :
        return str(self.opcode + " " + self.reg)

#base class for reading stdin
class InputInstruction(IOInstruction) :

    def exec(self) :
        dstreg = registerFile[self.reg]
        assert dstreg.type == self.dsttype, "Reading into register of type " + str(dstreg.type) + " when expecting " + str(self.dsttype)

        val = self.funcExec()

        dstreg.write(val)

    def funcExec(self) :
        return self.dsttype(input())

    @property
    def dsttype(self) :
        raise NotImplementedError("Implement in derived class")

#base class for writing to stdout
class OutputInstruction(IOInstruction) :

    def exec(self) :
        srcreg = registerFile[self.reg]
        assert srcreg.type == self.srctype, "Writing register of type " + str(srcreg.type) + " when expecting " + str(self.srctype)

        val = srcreg.read()

        self.funcExec(val)

    def funcExec(self, val) :
        print (val)

    @property
    def srctype(self) :
        raise NotImplementedError("Implement in derived class")

###### Instructions ######

#map opcodes (in text) to class associated with instruction
opCodeMap = {}

#decorator for concrete instructions to set up opcode map

class concreteInstruction :
    def __init__(self, opcode) :
        self.opcode = opcode

    def __call__(self, cls) :
        opCodeMap[self.opcode] = cls

@concreteInstruction('ADD')
class AddInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 + s2

@concreteInstruction('SUB')
class SubInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 - s2

@concreteInstruction('MUL')
class MulInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 * s2

@concreteInstruction('DIV')
class DivInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 // s2      

@concreteInstruction('REM')
class RemInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 % s2

@concreteInstruction('SLT')
class SltInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return 1 if s1 < s2 else 0

@concreteInstruction('AND')
class AndInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 & s2

@concreteInstruction('OR')
class OIRInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 | s2

@concreteInstruction('XOR')
class XoIRInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 ^ s2

@concreteInstruction('SLL')
class SllInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 << (s2 % 32)

@concreteInstruction('SRL')
class SrlInstruction(IRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 >> (s2 % 32)        

@concreteInstruction('ADDI')
class AddiInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 + imm

@concreteInstruction('ANDI')
class AndiInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 & imm

@concreteInstruction('OR')
class OriInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 | imm

@concreteInstruction('XOR')
class XoriInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 ^ imm

@concreteInstruction('SLTI')
class SltiInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return 1 if s1 < imm else 0

@concreteInstruction('SLLI')
class SlliInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 << (imm % 5)

@concreteInstruction('SRLI')
class SrliInstruction(IInstruction) :
    def funcExec(self, s1, imm) :
        return s1 >> (imm % 5)

@concreteInstruction('LUI')
class LuiInstruction(IUInstruction) :
    def funcExec(self, imm) :
        return imm << 12

@concreteInstruction('MV')
class MvInstruction(IORInstruction) :
    def funcExec(self, s1) :
        return s1

@concreteInstruction('NOT')
class NotInstruction(IORInstruction) :
    def funcExec(self, s1) :
        return ~s1

@concreteInstruction('FADD.S')
class FaddInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 + s2

@concreteInstruction('FSUB.S')
class FsubInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 - s2

@concreteInstruction('FMUL.S')
class FmulInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 * s2

@concreteInstruction('FDIV.S')
class FdivInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 / s2

@concreteInstruction('FMIN.S')
class FminInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 if s1 < s2 else s2

@concreteInstruction('FMAX.S')
class FmaxInstruction(FRInstruction) :
    def funcExec(self, s1, s2) :
        return s1 if s1 > s2 else s2        

@concreteInstruction('FSQRT.S')
class FsqrtInstruction(FORInstruction) :
    def funcExec(self, s1) :
        return s1 ** 0.5

@concreteInstruction('FLT.S')
class FltInstruction(FCmpInstruction) :
    def funcExec(self, s1, s2) :
        return 1 if s1 < s2 else 0

@concreteInstruction('FLE.S')
class FleInstruction(FCmpInstruction) :
    def funcExec(self, s1, s2) :
        return 1 if s1 <= s2 else 0

@concreteInstruction('FEQ.S')
class FeqInstruction(FCmpInstruction) :
    def funcExec(self, s1, s2) :
        return 1 if s1 == s2 else 0        


@concreteInstruction('LW')
class LwInstruction(LDInstruction) :
    @property
    def dsttype(self) :
        return int

@concreteInstruction('SW')
class SwInstruction(STInstruction) :
    @property
    def srctype(self) :
        return int

@concreteInstruction('FLW')
class FlwInstruction(LDInstruction) :
    @property
    def dsttype(self) :
        return float

@concreteInstruction('FSW')
class FswInstruction(STInstruction) :
    @property
    def srctype(self) :
        return float

#### Custom instructions -- not actually part of RISC-V instruction set ####

#store FP immediate to register
@concreteInstruction('FIMM.S')
class FimmInstruction(FUInstruction) :
    def funcExec(self, imm) :
        return imm

#move floating point to integer
@concreteInstruction('FMOVI.S')
class FmoviInstruction(FORInstruction) :
    def funcExec(self, src1) :
        return int(src1)

    @property
    def dsttype(self) :
        return float

#move integer to floating point
@concreteInstruction('IMOVF.S')
class ImovfInstruction(FORInstruction) :
    def funcExec(self, src1) :
        return float(src1)

    @property
    def srctype(self) :
        return float

#read integer from stdin
@concreteInstruction('GETI')
class GetiInstruction(InputInstruction) :
    @property
    def dsttype(self) :
        return int

#read float from stdin
@concreteInstruction('GETF')
class GetfInstruction(InputInstruction) :
    @property
    def dsttype(self) :
        return float       

@concreteInstruction('PUTI')
class PutiInstruction(OutputInstruction) :
    @property
    def srctype(self) :
        return int

@concreteInstruction('PUTF')
class PutfInstruction(OutputInstruction) :
    @property
    def srctype(self) :
        return float        

@concreteInstruction('PUTS')
class PutsInstruction(IOInstruction) :
    def __init__(self, reg, opcode) :
        self.reg = reg
        self.opcode = opcode

    def exec(self) :
        addr = registerFile[self.reg].read()
        assert (addr >= memory.strings[0] and addr < memory.strings[1]), "Writing string from a bad address"

        print(memory[addr])
        

#### unimplemented instructions ####
@concreteInstruction('AUIPC')
class AuipcInstruction(IUInstruction) :
    pass

@concreteInstruction('SLTIU')
class SltiuInstruction(IInstruction) :
    pass

@concreteInstruction('SRAI')
class SraiInstruction(IInstruction) :
    pass

@concreteInstruction('SLTU')
class SltuInstruction(IRInstruction) :
    pass

@concreteInstruction('SRA')
class SraInstruction(IRInstruction) :
    pass

@concreteInstruction('MULH')
class MulhInstruction(IRInstruction) :
    pass

@concreteInstruction('MULHSU')
class MulhsuInstruction(IRInstruction) :
    pass

@concreteInstruction('MULHU')
class MulhuInstruction(IRInstruction) :
    pass

@concreteInstruction('DIVU')
class DivuInstruction(IRInstruction) :
    pass

@concreteInstruction('REMU')
class RemuInstruction(IRInstruction) :
    pass

###### Parsing ######

#Parse the instruction and generate the right derived instruction from it
#The instruction is a single instruction string
def parseInstruction(inst) :
    base = inst.strip()
    opcode = re.match(r'(\S+)', base)[0]
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

    addr1 = 0x40000000
    addr2 = 0x40000004
    registerFile['a0'].write(addr1)
    registerFile['a1'].write(addr2)

    memory[0x10000000] = "Hello World"
    registerFile['a2'].write(0x10000000)

    insts = [
        'ADD t4, t0, t1',
        'ADD t5, t2, t3',
        'MUL t6, t4, t5',
        'ADDI t7, t6, 23',
        'LUI t8, 100',
        'FIMM.S f1, 2.5',
        'FMUL.S f2, f1, f1',
        'FSQRT.S f3, f2',
        'FLT.S t10, f3, f2',
        'SW t8, 0(a0)',
        'FSW f3, 0(a1)',
        'LW t11, 0(a0)',
        'FLW f4, 0(a1)',
        'PUTI t4',
        'PUTF f4',
        'GETI t4',
        'GETF f1',
        'PUTS a2'
    ]
    ops = [parseInstruction(i) for i in insts]
    for o in ops :
        print(o)
        o.exec()

    print(registerFile['t4'])
    print(registerFile['t5'])
    print(registerFile['t6'])
    print(registerFile['t7'])
    print(registerFile['t8'])
    print(registerFile['f1'])
    print(registerFile['f2'])
    print(registerFile['f3'])  
    print(registerFile['t10'])  

    print("Memory at " + hex(addr1) + ": " + str(memory[addr1]))
    print("Memory at " + hex(addr2) + ": " + str(memory[addr2]))

    print(registerFile['t11'])  
    print(registerFile['f4'])  


if __name__ == '__main__' :
    testExecList()
