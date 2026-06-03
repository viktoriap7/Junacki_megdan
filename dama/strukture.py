class Stek:
    def __init__(self):
        self.pod=[]
        self.size=0;
    def push(self,a):
        self.pod(a)
        self.size+=1
    def pop(self):
        if self.size==0:
            print("Prazan stek")
            return -1
        return self.pod.pop()
    def top(self):
        if self.size==0:
            print("Prazan stek")
            return -1
        return self.pod[-1]

class Dek:
    def __init__(self):
        self.kapacitet=5
class Stablo:
    def __init__(self):
        pass
