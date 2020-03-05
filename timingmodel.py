class defaultTimingModel :
    def __init__(self) :
        self.elapsedTime = 0
        pass

    def exec(self, inst) :
        pass

    def cacheExec(self, inst, address) :
        pass

    def getTotalTime(self) :
        return self.elapsedTime

class basicTimingModel(defaultTimingModel) :
    def __init__(self) :
        self.timingMap = {}
        self.elapsedTime = 0

    def exec(self, inst) :
        try :
            self.elapsedTime += inst.latency
        except AttributeError :
            self.elapsedTime += 1

    def cacheExec(self, inst, address) :
        self.exec(inst)