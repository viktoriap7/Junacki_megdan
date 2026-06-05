import pygame
from dama.const import *

class Figura:
    def __init__(self,indeks,boja):
        self.indeks=indeks 
        """ tabla4x8 """
        self.marko=False
        self.kralj=False
        self.boja=boja
        self.oklop=0
        self.topuz=False
        self.topuz_brojac=False
        self.sarac=False
        if boja==CRVENA:
            self.pravac=1
        else:
            self.pravac=-1
        """ tabla 8x8 """
        self.x=0
        self.y=0
    def postavi_oklop(self):
        if self.marko==True:
            self.oklop=2
        else:
            self.oklop=1
    def postavi_sarca(self):
        self.sarac=True
    def postavi_marka(self):
        self.marko=True
    def krunisi(self):
        self.kralj=True
    def postavi_topuz(self):
        self.topuz=True
    def postavi_topuz_br(self):
        self.topuz_brojac=True
    def __str__(self):
        boja=""
        if self.boja==CRVENA:
            boja="c"
        else:
            boja="p"
        if self.marko:
            return boja+";m"
        else:
            return boja
    def __repr__(self):
        return self.__str__()
    def rac_pozicija(self):
        self.y=RAZMAK_VIS+KVADRAT*(self.indeks//4)+KVADRAT//2
        pomjeraj=0
        if (self.indeks//4)%2==0:
            self.x=RAZMAK_SIR+KVADRAT*((self.indeks%4)*2)+KVADRAT//2
        else:
            self.x=RAZMAK_SIR+KVADRAT*((self.indeks%4)*2+1)+KVADRAT//2
        """ print("Figura: "+str(self.x)+" "+str(self.y)+"\n") """
    def nacrtaj(self,proz):
        pygame.draw.circle(proz,SIVA,(self.x,self.y),KVADRAT//3+2)
        pygame.draw.circle(proz,self.boja,(self.x,self.y),KVADRAT//3)
    
    def pomjeri(self,indeks):
        self.indeks=indeks
        self.rac_pozicija()
    