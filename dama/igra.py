import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.figura import Figura
class Igra:
    def __init__(self, proz):
        self.tren=None
        self.tabla=Tabla()
        self.na_redu=PLAVA
        self.pokreti={}
        self.proz=proz
    def update(self):
        self.tabla.nacrtaj(self.proz)
        pygame.display.update()
    def moguci_koraci(self):
        if self.na_redu==CRVENA:
            moguca_polja={}
            for i in range(32):
                if isinstance(self.tabla.polozaji[i],Figura) and self.tabla.polozaji[i].boja==CRVENA:
                    if (i//4)%2==0:#PARNI RED
                        if i%4==0:
                            self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4)-1,moguca_polja)
                        self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4),moguca_polja)
                    else: #NEPARNI RED
                        if i%4==3:
                            self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4)+1,moguca_polja)
                        self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4),moguca_polja)
                        
                        
    def provjeri_polje(self,fig,polje,moguca_polja):
        if self.tabla.polozaji[polje]==0:
            moguca_polja.append(polje)
        else:
            if fig.boja==self.tabla.polozaji[polje].boja:
                if fig.sarac==True:
                    self.provjeri_polje_iza()
            else:
                if fig.topuz_brojac==True:
                    moguca_polja.append(polje)
                self.provjeri_polje_iza()
    def provjeri_polje_iza(self):
        pass
