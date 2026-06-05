

class polje:
    def __init__(self):
        self
    
    def rac_pozicija(self):
        self.y=RAZMAK_VIS+KVADRAT*(self.indeks//4)+KVADRAT//2
        pomjeraj=0
        if (self.indeks//4)%2==0:
            self.x=RAZMAK_SIR+KVADRAT*((self.indeks%4)*2)+KVADRAT//2
        else:
            self.x=RAZMAK_SIR+KVADRAT*((self.indeks%4)*2+1)+KVADRAT//2
        """ print("Figura: "+str(self.x)+" "+str(self.y)+"\n") """