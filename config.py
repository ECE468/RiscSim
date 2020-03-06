import machine
import timingmodel

machine = machine.Machine(numIntRegisters = 64, numFloatRegisters = 64, timingModel = timingmodel.basicTimingModel)