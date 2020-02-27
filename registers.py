numIntRegisters = 64 #TODO: make this a configurable number, at least 32
numFloatRegisters = 64 #TODO: make this a configurable number, at least 32
numRegisters = numIntRegisters + numFloatRegisters

class Register :
    def __init__(self) :
        self.value = None
        self.name = None
        self.type = None

    def read(self) :
        return self.value

    def write(self, value) :
        if (type(value) != self.type) :
            raise(TypeError('Writing data of type ' + str(type(value)) + ' to register ' + self.name + ' which holds type ' + str(self.type)))
        self.value = value

    def __repr__(self) :
        return 'Register ' + self.name

    def __str__(self) :
        return str(self.value)

class IRegister(Register) :
    def __init__(self, name) :
        super().__init__()
        self.value = 0
        self.name = name
        self.type = int

class FRegister(Register) :
    def __init__(self, name) :
        super().__init__()
        self.value = 0.0
        self.name = name
        self.type = float

#Create register file
registerFile = {}

#initialize integer registers
for i in range(numIntRegisters) :
    name = 'x' + str(i)
    registerFile[name] = IRegister(name)

#Standard integer register aliases
registerFile['zero'] = registerFile['x0']
registerFile['ra'] = registerFile['x1']
registerFile['sp'] = registerFile['x2']
registerFile['gp'] = registerFile['x3']
registerFile['tp'] = registerFile['x4']
registerFile['t0'] = registerFile['x5']
registerFile['t1'] = registerFile['x6']
registerFile['t2'] = registerFile['x7']
registerFile['s0'] = registerFile['x8']
registerFile['fp'] = registerFile['x8']
registerFile['s1'] = registerFile['x9']
registerFile['a0'] = registerFile['x10']
registerFile['a1'] = registerFile['x11']
registerFile['a2'] = registerFile['x12']
registerFile['a3'] = registerFile['x13']
registerFile['a4'] = registerFile['x14']
registerFile['a5'] = registerFile['x15']
registerFile['a6'] = registerFile['x16']
registerFile['a7'] = registerFile['x17']
registerFile['s2'] = registerFile['x18']
registerFile['s3'] = registerFile['x19']
registerFile['s4'] = registerFile['x20']
registerFile['s5'] = registerFile['x21']
registerFile['s6'] = registerFile['x22']
registerFile['s7'] = registerFile['x23']
registerFile['s8'] = registerFile['x24']
registerFile['s9'] = registerFile['x25']
registerFile['s10'] = registerFile['x26']
registerFile['s11'] = registerFile['x27']
registerFile['t3'] = registerFile['x28']
registerFile['t4'] = registerFile['x29']
registerFile['t5'] = registerFile['x30']
registerFile['t6'] = registerFile['x31']

#alias any extra integer registers
for i in range(numIntRegisters - 32) :
    registerFile['t' + str(7 + i)] = registerFile['x' + str(32 + i)]

#initialize floating point registers
for f in range(numFloatRegisters) :
    name = 'f' + str(f)
    registerFile[name] = FRegister(name)    

#standard floating point register aliases
for i in range(0, 8) :
    registerFile['ft' + str(i)] = registerFile['f' + str(i)]

registerFile['fs0'] = registerFile['f8']
registerFile['fs1'] = registerFile['f9']

for i in range(0, 8) :
    registerFile['fa' + str(i)] = registerFile['f1' + str(i)]

for i in range(2, 12) :
    registerFile['fs' + str(i)] = registerFile['f' + str(16 + i)]

for i in range(8, 12) :
    registerFile['ft' + str(i)] = registerFile['f' + str(20 + i)]

#alias any extra floating point registers
for f in range(numFloatRegisters - 32) :
    registerFile['ft' + str(12 + f)] = registerFile['f' + str(32 + f)]


if __name__ == '__main__' :
    print(numRegisters)
    print(registerFile)

    registerFile['t3'].write(4)
    print(registerFile['x28']) #should print 4

    registerFile['f3'].write(5.0)
    print(registerFile['ft3']) #should print 5.0