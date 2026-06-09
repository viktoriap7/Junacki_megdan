import pygame
from dama.const import *

class Figura:
    def __init__(self,indeks,boja):
        self.indeks=indeks 
        """ tabla4x8 """
        self.marko=False
        self.kralj=False
        self.boja=boja
        self.oklop=False
        self.oklop_brojac=0
        self.topuz=False
        self.topuz_brojac=0
        self.sarac=False
        self.obrve=False
        self.zaledjena=0
        if boja==CRVENA:
            self.pravac=1
        else:
            self.pravac=-1
        """ tabla 8x8 """
        self.x=0
        self.y=0
    def postavi_oklop(self):
        self.oklop=True
    def upotrebi_oklop(self):
        self.oklop=False
        if self.marko==True:
            self.oklop_brojac=2
        else:
            self.oklop_brojac=1
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
    def postavi_pogled(self):
        self.obrve=True
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
        if self.obrve:
            if self.boja==PLAVA:
                slika=OCI_PLAVI
            else:
                slika=OCI_CRVENI
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
        if self.zaledjena>0:
            x1=self.x-(KVADRAT//2)
            y1=self.y-(KVADRAT//2)
            x2=x1+KVADRAT
            y2=y1+KVADRAT
            pygame.draw.line(proz,BIJELA,(x1,y1),(x2,y2),3)
            pygame.draw.line(proz,BIJELA,(x2,y1),(x1,y2),3)
        
    def ispisi_atribute(self,proz):
        if self.zaledjena>0:
            text="Zaleđena figura:\n"
        else:
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
            text+="-Ima šarca\n"
        if self.oklop:
            text+="-Ima štit\n"
        linije=text.split('\n')
        trenutno_y=ATRIBUTI_VIS
        for linija in linije:
            if linija!="":
                sve=FONT.render(linija,True,BIJELA)
                proz.blit(sve,(ATRIBUTI_SIR,trenutno_y))
                trenutno_y+=sve.get_height()+5
        
        if self.oklop:
            
            pygame.draw.rect(proz,CRNA,pygame.Rect(ATRIBUTI_SIR,ATRIBUTI_STIT_VIS,ATRIBUTI_DUGME_SIR,ATRIBUTI_DUGME_VIS),2)
            #pygame.draw.rect(self.proz,CRNA,pygame.Rect(DESNO_POPUP_X,DESNO_POPUP_Y,DUGME_SIR_POPUP,DUGME_VIS_POPUP),2)
        
            tekst_dugmeta = FONT.render("Upotrebi oklop", True, BIJELA)
            proz.blit(tekst_dugmeta, (ATRIBUTI_SIR + 10, ATRIBUTI_STIT_VIS + 8))
        if self.obrve:
            pygame.draw.rect(proz,CRNA,pygame.Rect(ATRIBUTI_SIR,ATRIBUTI_OKO_VIS,ATRIBUTI_DUGME_SIR,ATRIBUTI_DUGME_VIS),2)
            #pygame.draw.rect(self.proz,CRNA,pygame.Rect(DESNO_POPUP_X,DESNO_POPUP_Y,DUGME_SIR_POPUP,DUGME_VIS_POPUP),2)
        
            tekst_dugmeta = FONT.render("Upotrebi pogled", True, BIJELA)
            proz.blit(tekst_dugmeta, (ATRIBUTI_SIR + 10, ATRIBUTI_OKO_VIS + 8))
            
        pygame.display.update()
    def pomjeri_fig(self,indeks):
        self.indeks=indeks
        self.rac_pozicija()
    