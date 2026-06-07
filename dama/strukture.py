import random

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
        self.pod=[None]*5
        self.polozaj=0

        for i in range(5):
            self.pod[i]=2
            #self.pod[i]=random.randint(1,3)
    def rotiraj_dek(self):
        self.polozaj=(self.polozaj+1)%self.kapacitet
        print("Rotiran dek")
    def ukloni_prvi(self):
        a=self.pod[self.polozaj]
        self.pod[self.polozaj]=random.randint(1,3)
        #self.rotiraj_dek()
        self.ispis()
        return a
    def ukloni_zadnji(self):
        a=self.pod[(self.polozaj-1)%self.kapacitet]
        self.pod[(self.polozaj-1)%self.kapacitet]=random.randint(1,3)
        #self.rotiraj_dek()
        self.ispis()
        return a
    def vidi_prvi(self):
        return self.pod[self.polozaj]
    def vidi_zadnji(self):
        return self.pod[(self.polozaj-1)%self.kapacitet]
    def ispis(self):
        print("kap: "+str(self.kapacitet))
        print("dek: [",end="")
        for i in self.pod:
            print(str(i)+" ",end="")
        print("]")
class Cvor:
    __slots__ = 'rod', 'dijete', 'pod'
    def __init__(self,pod):
        self.rod=None
        self.dijete=[]
        self.pod=pod
    def roditelj(self,cvor):
        self.rod=cvor
    def dodaj_dijete(self,dijete):
        dijete.roditelj(self)
        self.dijete.append(dijete)
            
class Stablo:
    def __init__(self):
        self.korijen=None
    def preorder(self,cvor):
        print(cvor.pod)
        for child in cvor.dijete:
            self.preorder(child)


def testiraj_dek():    
    dek=Dek()
    dek.dodaj_prvi(1)
    dek.ispis()
    dek.dodaj_zadnji(2)
    dek.ispis()
    dek.dodaj_zadnji(3)
    dek.ispis()
    dek.dodaj_zadnji(4)
    dek.ispis()
    dek.dodaj_prvi(5)
    dek.ispis()
    dek.dodaj_zadnji(6)
    dek.ispis()
    dek.dodaj_prvi(7)
    dek.ispis()
def testitaj_stablo():
    pass
#testiraj_dek()