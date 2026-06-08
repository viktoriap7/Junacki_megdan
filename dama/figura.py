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
        self.topuz_brojac=0
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
        print("--- DETEKTIVSKI ISPIS ---")
        print("Funkcija krunisi() je UPRAVO POKRENUTA za indeks: " + str(self.indeks))
        print("Pre krunisanja, self.kralj je: " + str(self.kralj))
        print("Pre krunisanja, self.marko je: " + str(self.marko))
        self.kralj=True
    def postavi_topuz(self):
        self.topuz=True
        self.topuz_brojac=1
    def postavi_topuz_br(self):
        self.topuz_brojac=1
    def __str__(self):
        boja=""
        if self.boja==CRVENA:
            boja="c"
        else:
            boja="p"
        if self.marko:
            return boja+";m"
        if self.kralj:
            return boja+";k"
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

        slika=None
        if self.topuz:
            if self.boja==PLAVA:
                slika=TOPUZ_PLAVA
            else:
                slika=TOPUZ_CRVENA

        if self.oklop>0:
            if self.boja==PLAVA:
                slika=STIT_PLAVA
            else:
                slika=STIT_CRVENA

        if self.sarac:
            if self.boja==PLAVA:
                slika=KONJ_PLAVI
            else:
                slika=KONJ_CRVENI

        if self.kralj:
            pygame.draw.circle(proz,BIJELA,(self.x,self.y),KVADRAT//3+4)
            if self.boja==PLAVA:
                slika=KRALJ_PLAVA
            else:
                slika=KRALJ_CRVENA
        
        if self.marko:
            pygame.draw.circle(proz,ZUTA,(self.x,self.y),KVADRAT//3+4)
            if self.boja==PLAVA:
                slika=MARKO_PLAVI
            else:
                slika=MARKO_CRVENI
        
        if slika:    
            proz.blit(slika, (self.x - slika.get_width() // 2 -1, self.y - slika.get_height() // 2 -1))
        else:
            pygame.draw.circle(proz,SIVA,(self.x,self.y),KVADRAT//3+2)
            pygame.draw.circle(proz,self.boja,(self.x,self.y),KVADRAT//3)
    
    def ispisi_atribute(self,proz):
        text="Figura:"
        if self.marko:
            text+=" Kraljević Marko"
        elif self.kralj:
            text+=" Kraljević"
        else:
            text+=" Junak"
        text+="\n"
        if self.topuz:
            text+="-Ima topuz\n"
        if self.sarac:
            text+="-Ima sarca\n"
        
        linije=text.split('\n')
        trenutno_y=ATRIBUTI_VIS
        for linija in linije:
            if linija!="":
                sve=FONT.render(linija,True,BIJELA)
                proz.blit(sve,(ATRIBUTI_SIR,trenutno_y))
                trenutno_y+=sve.get_height()+5
        pygame.display.update()
    def pomjeri_fig(self,indeks):
        self.indeks=indeks
        self.rac_pozicija()
    