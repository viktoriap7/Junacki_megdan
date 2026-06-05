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
    def __init__(self,k):
        self.kapacitet=k
        self.pod=[None]*self.kapacitet
        self.size=0
        self.prvi=0
    def resize(self):
        self.kapacitet=self.kapacitet*2
        novi_pod=[None]*self.kapacitet
        """ for i in range(self.size):
            novi_pod[i]=self.pod[i]
        self.pod=novi_pod
         """
        razmak=self.size-self.prvi
        for i in range(self.prvi):
            novi_pod[i]=self.pod[i]
        for i in range(razmak,0,-1):
            novi_pod[self.kapacitet-i]=self.pod[self.size-i]
        self.pod=novi_pod
        self.prvi=self.kapacitet-razmak
    def dodaj_prvi(self,a):
        print("dodajem na pocetak:"+str(a))
        if self.size==self.kapacitet:
            self.resize()
        self.prvi=(self.prvi-1)%self.kapacitet
        self.pod[self.prvi]=a
        self.size+=1
    def dodaj_zadnji(self,a):
        print("dodajem na zadnji:"+str(a))
        if self.size==self.kapacitet:
            self.resize()
        self.pod[(self.prvi+self.size)%self.kapacitet]=a
        self.size+=1
    """ treba dodati sklanjanja """
    def ukloni_prvi(self):
        if self.size==0:
            print("prazan dek")
            return None
        a=self.pod[self.prvi]
        self.pod[self.prvi]=None
        self.prvi=(self.prvi+1)%self.kapacitet
        self.size-=1
        """ if self.kapacitet==self.size*2:
            novi_pod=[None]*self.size
            razmak=self.kapacitet-self.prvi
            for i in range() """
    def ukloni_zadnji(self):
        if self.size==0:
            print("prazan dek")
            return None
        a=self.pod[(self.prvi+self.size)%self.kapacitet]
        self.pod[(self.prvi+self.size)%self.kapacitet]=None
        self.size-=1
    def ispis(self):
        print("kap: "+str(self.kapacitet))
        print("[",end="")
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
    dek=Dek(3)
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