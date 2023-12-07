from memory import Memory
from registers import IRegister
from registers import FRegister
import timingmodel
import program
import config
import machine
import sys
import argparse

if __name__ == '__main__' :

    parser = argparse.ArgumentParser("Simulate RISC-V execution",add_help=True)
    parser.add_argument("-m", dest="memuse", action="store_true", default=False,
                        help="show memory usage")
    parser.add_argument("asm", help="assembly file to simulate")
    parser.add_argument("nregs", nargs="?", help="number of registers to simulate")
    parser.add_argument("-d",dest="use_debug", help="set to 1 to print assembly lines as they are being executed")

    args = parser.parse_args()

    if args.nregs :
        if int(args.nregs) < 32 :
            print("Cannot initialize simulator with fewer than 32 registers")
            sys.exit(1)
        print("Initializing machine with " + args.nregs + " registers")
        config.machine = machine.Machine(numIntRegisters = int(args.nregs), numFloatRegisters = int(args.nregs), timingModel = timingmodel.basicTimingModel)
    else :
        print("Using default machine configuration with 256 registers")

    p = program.Program()
    p.buildCodeFromFile(args.asm)

    config.machine.execProgram(p, args.memuse, useDebug=args.use_debug)
