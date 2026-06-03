import pygame
from dama.const import *
from dama.figura import *
class Tabla:
    def __init__(self):
        self.polozaji=[]
        self.tren=None
        self.bijele_fig=12
        self.crne_fig=12
        self.bijeli_marko_br=0
        self.crni_marko_br=0
    def prikazi_tablu(self):
        print("Stanje Table")
        for red in range(BR_RED):
            """ tabela 4x8 """
            for kol in range(BR_KOL//2):
                print(str(self.polozaji[red*4+kol])+" ",end="")
            print("")
    def nacrtaj_kvadrate(self,proz):
        proz.fill(SIVA)
        boja=SIVA
        for red in range(BR_RED):
            for kol in range(BR_KOL):
                if((red+kol)%2==0):
                    boja=CRNA
                else:
                    boja=BIJELA
                
                pygame.draw.rect(proz,boja,(RAZMAK_SIR+kol*KVADRAT,RAZMAK_VIS+red*KVADRAT,KVADRAT,KVADRAT))
    def nacrtaj_figure(self,proz):
        for elem in self.polozaji:
            if(isinstance(elem,Figura)):
                elem.nacrtaj(proz)
            
    def napravi_tablu(self,proz):
        for red in range(BR_RED):
            """ tabela 4x8 """
            for kol in range(BR_KOL//2):
                if red<3:
                    """ print("indeks:"+str(red*4+kol)+"\n") """
                    fig=Figura(red*4+kol,CRVENA)
                    fig.rac_pozicija()
                    fig.nacrtaj(proz)
                    self.polozaji.append(fig)
                elif red>4:
                    fig=Figura(red*4+kol,PLAVA)
                    fig.rac_pozicija()
                    fig.nacrtaj(proz)
                    self.polozaji.append(fig)
                else:
                    self.polozaji.append(0)
        self.prikazi_tablu()
    def nacrtaj(self,proz):
        self.nacrtaj_kvadrate(proz)
        self.nacrtaj_figure(proz)
        self.prikazi_tablu()
    def pomjeri(self,fig,indeks):
        self.polozaji[fig.indeks],self.polozaji[indeks]=self.polozaji[indeks],self.polozaji[fig.indeks]
        fig.pomjeri(indeks)
        if indeks//4==0 or indeks//4==7:
            fig.postavi_marka()
            if fig.boja==CRVENA:
                self.crni_marko_br+=1
            elif fig.boja==PLAVA:
                self.bijeli_marko_br+=1
        self.prikazi_tablu()
    def vrati_fig(self,indeks):
        return self.polozaji[indeks]