import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.figura import Figura

class Igra:
    def __init__(self, proz):
        self.tren=None
        self.tabla=Tabla()
        self.na_redu=PLAVA
        self.moguci_koraci=[]
        self.proz=proz
    def update(self):
        self.tabla.nacrtaj(self.proz)
        pygame.display.update()
    def zamjeni_na_redu(self):
        if self.na_redu==CRVENA:
            self.na_redu==PLAVA
            
            print("Na redu: plavi" )
        else:
            print("Na redu: crveni" )
            self.na_redu=CRVENA
            
    def dobij_indeks_od_misa(self,poz): #poz=koordinate klika misa
        x,y=poz
        x=x-RAZMAK_SIR
        x=x//KVADRAT
        y=y-RAZMAK_VIS
        y=y//KVADRAT
        if x%2==0 and y%2==0:
            return (y*4)+(x//2)
        elif x%2==1 and y%2==1:
            return (y*4)+((x-1)//2)
        else:
            return -1

    def odabir_misem(self,poz):
        if self.tren:
            print("vec je nesto izabrano "+str(self.tren)+" "+str(self.tren.indeks))
            indeks=self.dobij_indeks_od_misa(poz)
            print("Indeks: "+str(indeks))
            print("moguci koraci:"+str(self.moguci_koraci))
            if indeks!=-1 and self.tabla.polozaji[indeks]!=0:
                if self.tabla.polozaji[indeks].boja==self.tren.boja:
                    print("promjena odabranog")
                    self.tren=self.tabla.polozaji[indeks]
                    self.nacrtaj_moguce_korake()
            elif indeks in self.moguci_koraci:
                print("koran na "+str(indeks))
                self.pokusaj_pomjeriti(indeks)            
                #self.zamjeni_na_redu()
            else:
                self.tren=None
            print("Tren: "+str(self.tren)+" na redu:"+str(self.na_redu))
        else:
            print("nema nista izabrano")
            indeks=self.dobij_indeks_od_misa(poz)
            if indeks!=-1 and self.tabla.polozaji[indeks]!=0:
                if self.tabla.polozaji[indeks].boja==self.na_redu:
                    self.tren=self.tabla.polozaji[indeks]
                    print("izabran "+str(self.tren)+" "+str(self.tren.indeks))
                    self.nacrtaj_moguce_korake()
            pygame.display.update()
    def nacrtaj_moguce_korake(self):
        print("Izabrana fig:"+str(self.tren)+" na mjestu "+str(self.tren.indeks))
        self.moguci_koraci=self.dobij_moguce_korake()
        print("Moguci koraci:"+str(self.moguci_koraci))
        #iscrtati moguce korake
        for polje in self.moguci_koraci:
            #racunam koordinate sredine kruga
            y=RAZMAK_VIS+KVADRAT*(polje//4)+KVADRAT//2
            if (polje//4)%2==0:
                x=RAZMAK_SIR+KVADRAT*((polje%4)*2)+KVADRAT//2
            else:
                x=RAZMAK_SIR+KVADRAT*((polje%4)*2+1)+KVADRAT//2
            pygame.draw.circle(self.proz,ZELENA,(x,y),10)

    def pokusaj_pomjeriti(self,indeks):
        #polje=self.tabla.vrati_fig(indeks)
        #PROVJERAVA DA LI JE NESTO NA TABLI IZABRANO
        #I DA LI JE TU MOGUCE POMJERITI SE
        #if self.tren and indeks in self.moguci_koraci:
        self.tabla.pomjeri(self.tren,indeks)
        self.tabla.nacrtaj(self.proz)
        self.zamjeni_na_redu()
        self.tren=None
        #else:
        #    return False
        #return True

    def dobij_moguce_korake(self):
        moguca_polja=[]
        if self.na_redu==CRVENA:
            #GRESKA: NE ZNA KOJU FIGURU DA POMJERI RACUNAR
            #NIJE ODREDJEN TREN
            #for i in range(32):
                #if isinstance(self.tabla.polozaji[i],Figura) and self.tabla.polozaji[i].boja==CRVENA:
            i=self.tren.indeks
            if (i//4)%2==0:#PARNI RED
                if i%4!=0:
                    pol=i+(self.tabla.polozaji[i].pravac*4)-1
                    if 0<=pol<=31: 
                        self.provjeri_polje(self.tabla.polozaji[i],pol,moguca_polja)
                pol=i+(self.tabla.polozaji[i].pravac*4)
                if 0<=pol<=31:
                    self.provjeri_polje(self.tabla.polozaji[i],pol,moguca_polja)
            else: #NEPARNI RED
                if i%4!=3:
                    self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4)+1,moguca_polja)
                self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4),moguca_polja)
        elif self.na_redu==PLAVA:
            i=self.tren.indeks
            if (i//4)%2==0:#PARNI RED
                if i%4!=0:
                    pol=i+(self.tabla.polozaji[i].pravac*4)-1
                    if 0<=pol<=31: 
                        self.provjeri_polje(self.tabla.polozaji[i],pol,moguca_polja)
                pol=i+(self.tabla.polozaji[i].pravac*4)
                if 0<=pol<=31:
                    self.provjeri_polje(self.tabla.polozaji[i],pol,moguca_polja)
            else: #NEPARNI RED
                if i%4!=3:
                    self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4)+1,moguca_polja)
                self.provjeri_polje(self.tabla.polozaji[i],i+(self.tabla.polozaji[i].pravac*4),moguca_polja)

        return moguca_polja                
                        
    def provjeri_polje(self,fig,polje,moguca_polja):
        if self.tabla.polozaji[polje]==0:
            moguca_polja.append(polje)
        else:
            if fig.boja==self.tabla.polozaji[polje].boja:
                if fig.sarac==True:
                    boja_nove_fig=self.tabla.polozaji[polje].boja
                    self.moguce_polje_iza(fig,boja_nove_fig,polje,moguca_polja)
            else:
                if fig.topuz_brojac==True:
                    moguca_polja.append(polje)
                
                boja_nove_fig=self.tabla.polozaji[polje].boja
                self.moguce_polje_iza(fig,boja_nove_fig,polje,moguca_polja)
    def moguce_polje_iza(self,fig,boja_nove_fig,polje,moguca_polja):
        
        if (polje//4)%2==0:
            if polje%4!=0:
                if abs(fig.indeks-polje)==4:
                    self.provjeri_polje_iza(fig,boja_nove_fig,polje +(fig.pravac*4)+1,moguca_polja)
                else:
                    self.provjeri_polje_iza(fig,boja_nove_fig,polje +(fig.pravac*4),moguca_polja)
    def provjeri_polje_iza(self,fig,boja_nove_fig,polje,moguce_polja):
        """ if fig.boja==boja_nove_fig:
            if self.tabla.polozaji[polje]==0:
                moguce_polja.append(polje)
        elif fig.boja!=boja_nove_fig:
            if  self.tabla.polozaji[polje]==0:
                moguce_polja.append(polje)
                #TREBA DODATI BRISANJE FIGURA
         """
        if  self.tabla.polozaji[polje]==0:
            moguce_polja.append(polje)
            if fig.boja!=boja_nove_fig:
                #BRISANJE
                pass        
