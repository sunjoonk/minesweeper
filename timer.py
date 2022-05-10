import time

class Timer:
    def __init__(self):
        self.startTime = time.time()
        self.passTime = 0
    
    def setTime(self):
        self.passTime = int(time.time() - self.startTime)

    def getTime(self):
        return self.passTime