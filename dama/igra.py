from copy import deepcopy
import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.figura import Figura
from dama.strukture import *
class Igra:
    def __init__(self, proz):
        self.tren=None
        self.tabla=Tabla()
        self.na_redu=PLAVA
        #rijecnik kljuc:indeks na koji fig staje, vrijednost:fig koju jede
        self.moguca_polja={}
        self.proz=proz
        self.broj_poteza=0
        self.lanac=False
        self.biranje=False
        self.dek_moci=Dek()
    def __deepcopy__(self, memo):
        # Kreiramo novu instancu klase bez pozivanja __init__-a
        nova_igra = self.__class__.__new__(self.__class__)
        
        # Obavezno ažuriraj memo rječnik kako bi izbjegla beskonačnu rekurziju
        memo[id(self)] = nova_igra
        
        # 1. REFERENCA (ne kopiramo ga, samo prenosimo vezu)
        nova_igra.proz = self.proz  
        
        nova_igra.tren = deepcopy(self.tren, memo)
        nova_igra.tabla = deepcopy(self.tabla, memo)
        nova_igra.moguca_polja = deepcopy(self.moguca_polja, memo)
        nova_igra.dek_moci = deepcopy(self.dek_moci, memo)
        nova_igra.na_redu = self.na_redu
        nova_igra.broj_poteza = self.broj_poteza
        nova_igra.lanac = self.lanac
        nova_igra.biranje = self.biranje
        
        return nova_igra
    def update(self):
        self.tabla.nacrtaj(self.proz)
        boja_teksta = BIJELA if self.na_redu == PLAVA else CRVENA
        ime_igraca = "PLAVI" if self.na_redu == PLAVA else "CRVENI"
        
        tekst_povrsina = FONT.render(f"Na redu: {ime_igraca}", True, boja_teksta)
        self.proz.blit(tekst_povrsina, (10, 10))
        pygame.display.update()
        
    def zamjeni_na_redu(self):
        if self.na_redu==CRVENA:
            self.na_redu=PLAVA
            print("Na redu: plavi"+str(self.na_redu) )
        else:
            self.na_redu=CRVENA
            print("Na redu: crveni"+str(self.na_redu) )
        self.dek_moci.rotiraj_dek()
            
    def dobij_indeks_od_misa(self,poz): #poz=koordinate klika misa
        x,y=poz
        if self.tren and self.tren.oklop and self.tren.boja == self.na_redu:
            if ATRIBUTI_SIR<=x<=ATRIBUTI_SIR+ATRIBUTI_DUGME_SIR and ATRIBUTI_STIT_VIS<=y<=ATRIBUTI_STIT_VIS+ATRIBUTI_DUGME_VIS:
                return -2
        if self.tren and self.tren.obrve and self.tren.boja == self.na_redu:
            if ATRIBUTI_SIR<=x<=ATRIBUTI_SIR+ATRIBUTI_DUGME_SIR and ATRIBUTI_OKO_VIS<=y<=ATRIBUTI_OKO_VIS+ATRIBUTI_DUGME_VIS:
                return -3
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
        if self.biranje:#kad se prikaze popup moci
            print("pop up moci prikazan")
            izabrano=self.dobij_stranu_moci_od_misa(poz)
            self.dodjeli_moc(izabrano)
            self.upravljaj_redom()
            self.broj_poteza=0
            return False
        else:
            if self.tren:
                    if self.lanac:
                        indeks=self.dobij_indeks_od_misa(poz)
                        if indeks in self.moguca_polja and self.moguca_polja[indeks]!=0:
                            self.pokusaj_pomjeriti(indeks)

                    else:    
                        print("vec je nesto izabrano "+str(self.tren)+" "+str(self.tren.indeks))
                        indeks=self.dobij_indeks_od_misa(poz)
                        print("Indeks: "+str(indeks))
                        print("moguci koraci:"+str(self.moguca_polja))
                        
                        if indeks==-2:                             #pritisnuto dugme oklopa
                            self.tren.upotrebi_oklop()
                            self.upravljaj_redom()
                            self.tabla.nacrtaj(self.proz)
                            pygame.display.update()
                            return True
                        if indeks==-3:
                            promadji_najblizu(self.tren,self.tabla.polozaji)
                            self.upravljaj_redom()
                            self.tabla.nacrtaj(self.proz)
                            pygame.display.update()
                            return True
                        elif indeks in self.moguca_polja:           #pomjeranje fig
                            self.pokusaj_pomjeriti(indeks)
                            if self.biranje:                
                                self.nacrtaj_biranje_moci()
                            return True
                        elif indeks!=-1 and self.tabla.polozaji[indeks]!=0:   #selektovanje druge fig
                            
                            if self.tabla.polozaji[indeks].boja==self.tren.boja:
                                print("promjena odabranog")
                                self.tren=self.tabla.polozaji[indeks]
        
                                self.tabla.nacrtaj(self.proz)
                                pygame.display.update()
                                self.nacrtaj_moguce_korake()
                        
                        else:                                       #odselektovanje
                            self.tren=None
                            self.tabla.nacrtaj(self.proz)
                            pygame.display.update()
                        print("Tren: "+str(self.tren)+" na redu:"+str(self.na_redu))
                        return False
            else:
                print("nema nista izabrano")
                indeks=self.dobij_indeks_od_misa(poz)
                if indeks!=-1 and self.tabla.polozaji[indeks]!=0:
                    self.tabla.polozaji[indeks].ispisi_atribute(self.proz)
                    if self.tabla.polozaji[indeks].boja==self.na_redu and self.tabla.polozaji[indeks].zaledjena==0:
                        self.tren=self.tabla.polozaji[indeks]
                        print("izabran "+str(self.tren)+" "+str(self.tren.indeks))
                        self.nacrtaj_moguce_korake()
                pygame.display.update()
                return False
    def nacrtaj_moguce_korake(self):
        self.tren.ispisi_atribute(self.proz)
        if self.tren.zaledjena==0:
            print("Izabrana fig crtanje:"+str(self.tren)+" na mjestu "+str(self.tren.indeks))
            self.dobij_moguce_korake()
            print("crtanje Moguci koraci:"+str(self.moguca_polja))
            #iscrtati moguce korake
            if self.lanac:              #za lancano prikazi samo polja koja pojedu nesto
                for polje in self.moguca_polja:
                    #racunam koordinate sredine kruga
                    if self.moguca_polja[polje]!=0:
                        y=RAZMAK_VIS+KVADRAT*(polje//4)+KVADRAT//2
                        if (polje//4)%2==0:
                            x=RAZMAK_SIR+KVADRAT*((polje%4)*2)+KVADRAT//2
                        else:
                            x=RAZMAK_SIR+KVADRAT*((polje%4)*2+1)+KVADRAT//2
                        pygame.draw.circle(self.proz,ZELENA,(x,y),10)

            else:                       #prikazi sve mogucnosti kretanja
                for polje in self.moguca_polja:
                    #racunam koordinate sredine kruga
                    y=RAZMAK_VIS+KVADRAT*(polje//4)+KVADRAT//2
                    if (polje//4)%2==0:
                        x=RAZMAK_SIR+KVADRAT*((polje%4)*2)+KVADRAT//2
                    else:
                        x=RAZMAK_SIR+KVADRAT*((polje%4)*2+1)+KVADRAT//2
                    pygame.draw.circle(self.proz,ZELENA,(x,y),10)
    def dobij_korake_koji_jedu(self):
        jedu=[]
        self.dobij_moguce_korake()
        for polje in self.moguca_polja:
            if self.moguca_polja[polje]!=0:
                jedu.append((self.tren.indeks,polje,self.moguca_polja[polje].indeks,None))
        return jedu
    def dobij_moguce_korake(self):
        self.moguca_polja = {}
        #U rijecniku cuva mjesto gdje ce stati: sta jede
        #print("igra:dobij_moguce_korake")
        if not self.tren:
            print("Nije nista izabrano")
            return
        i=self.tren.indeks
        osnovni_pravac=self.tren.pravac
        #ide u osnovnom pravcu

        #obicne fig
        if not self.tren.kralj:
            self.provjeri_dijagonale(self.tren,i,osnovni_pravac)
        elif self.tren.zaledjena==0:
        #vise polja i drugi pravac za kralja
            
            obrnuti_pravac=osnovni_pravac*-1
            self.provjeri_dijagonale_kralja(self.tren,i,osnovni_pravac)
            self.provjeri_dijagonale_kralja(self.tren,i,obrnuti_pravac)
            if self.tren.sarac or self.tren.topuz_brojac: # koristi tvoj naziv atributa iz figure
               # print("Kralj ima relikviju (Šarac/Topuz) - računam posebne korake...")
                self.provjeri_dijagonale(self.tren, i, osnovni_pravac)
                self.provjeri_dijagonale(self.tren, i, obrnuti_pravac)
        #print("\t tren:"+str(self.tren.indeks))
        #print("moguca polja: "+str(self.moguca_polja))
    def pokusaj_pomjeriti(self,indeks):
        print("korak na "+str(indeks))
        #self.pokusaj_pomjeriti(indeks)
        fig_za_jedednje=self.moguca_polja[indeks]
        #ako namjestu gdje stajemo postoji fig, iskoristen je topuz
        if self.moguca_polja[indeks]!=0:
            if self.tabla.polozaji[indeks]!=0:
                if self.tren.topuz_brojac>0:
                    self.tren.topuz_brojac-=1
        
        pojeo=self.tabla.pojedi_fig(fig_za_jedednje,self.tren.boja)
        self.tabla.pomjeri(self.tren,indeks) #pomjera figure mjenjanjem indeksa
        self.broj_poteza+=1
        self.tabla.nacrtaj(self.proz)
        if self.tren.indeks in self.tabla.oranje:
            self.biranje=True
            self.broj_poteza=0
        self.tabla.nacrtaj(self.proz)
        pygame.display.update()
        if pojeo:                           #ako igrac pojede nesto,ispitaj da li moze lancano
            self.lanac=True
            self.broj_poteza=0
            self.nacrtaj_moguce_korake()
            if any(v != 0 for v in self.moguca_polja.values()):
                print("Postoji figura koja se moze pojest")
            else:                                 #ako nema daljeg, igra drugi igrac
                self.upravljaj_redom()
        else:                                 #ako nije pojeo nista, igra drugi igrac
            self.upravljaj_redom()
    
    def upravljaj_redom(self):
        #self.tren=Figura
        if not self.biranje:
            self.zamjeni_na_redu()
            for fig in self.tabla.polozaji:
                if fig!=0: 
                    if fig.boja==self.na_redu and fig.oklop_brojac>0: 
                        #kada je neka boja na redu smanji njihove brojace
                        print("\t smanjen brojac oklopa")
                        fig.oklop_brojac-=1
                    if fig.boja!=self.na_redu and fig.zaledjena>0:
                        #kada je protivnik na redu smanji zaledjenost svojih figura
                        print("\todledjavaj")
                        fig.zaledjena-=1    
            if self.tren.topuz:
                self.tren.topuz_brojac=1
            self.tren=None
            self.lanac=False
            self.update()
    def provjeri_dijagonale(self, fig, i, pravac):
        """Pomocna funkcija koja provjerava dijagonale za zadati pravac kretanja"""
        if (i//4)%2==0:  # PARNI RED
            if i%4!=0:
                pol=i+(pravac*4)-1
                if 0<=pol<=31: 
                    self.provjeri_polje(fig,pol,pravac)
            pol=i+(pravac*4)
            if 0<=pol<=31:
                self.provjeri_polje(fig,pol,pravac)
        else:  # NEPARNI RED
            if i%4!=3:
                pol=i+(pravac*4)+1
                if 0<=pol<=31:
                    self.provjeri_polje(fig,pol,pravac)
            pol=i+(pravac*4)
            if 0<=pol<=31:
                self.provjeri_polje(fig, pol,pravac)    
                        
    def provjeri_polje(self,fig,polje,pravac):
        if self.tabla.polozaji[polje]==0:
            self.moguca_polja[polje]=0
            #print("prazno na indeksu "+str(polje))
        else:
            if fig.boja==self.tabla.polozaji[polje].boja:
                #print("ista boja na indeksu "+str(polje))
                if fig.sarac==True:
                    print("\tima sarca ")
                    boja_nove_fig=self.tabla.polozaji[polje].boja
                    self.moguce_polje_iza(fig,boja_nove_fig,polje,pravac)
            else:
                if self.tabla.polozaji[polje].oklop_brojac>0:
                    pass
                    #print("fig ima oklop na indeksu: "+str(fig.indeks))
                else:    
                    #print("razlicita boja na indeksu "+str(polje))
                    if fig.topuz_brojac>0:
                        print("\tima topuz ")
                        #U rijecniku cuva mjesto gdje ce stati: sta jede
                        self.moguca_polja[polje]=self.tabla.polozaji[polje]
                    
                    boja_nove_fig=self.tabla.polozaji[polje].boja
                    self.moguce_polje_iza(fig,boja_nove_fig,polje,pravac)
        
    def moguce_polje_iza(self,fig,boja_nove_fig,polje,pravac):
        #print("provjera polja iza")
        if (polje//4)%2==0: #Parni red
        #    print("\t parni red")
            if polje%4!=0:
                if abs(fig.indeks-polje)==4:
                    pol=polje +(pravac*4)-1
                    if 0<=pol<=31:
        #                print("\t pomjeraj 4 "+str((pravac*4)-1)+"="+str(pol))
                        self.provjeri_polje_iza(fig,boja_nove_fig,pol,polje)
                else:
                    pol=polje +(pravac*4)
                    if 0<=pol<=31:
        #                print("\t pomjeraj nije 4 "+str((pravac*4))+"="+str(pol))
                        self.provjeri_polje_iza(fig,boja_nove_fig,pol,polje)
        else: #neparni red
        #    print("\t neparni red")
            if polje%4!=3:
                if abs(fig.indeks-polje)==4:
                    pol=polje +(pravac*4)+1
                    if 0<=pol<=31:
        #                print("\t pomjeraj 4 "+str((pravac*4)+1)+"="+str(pol))
                        self.provjeri_polje_iza(fig,boja_nove_fig,pol,polje)
                else:
                    pol=polje +(pravac*4)
                    if 0<=pol<=31:
        #                print("\t pomjeraj nije 4 "+str((pravac*4))+"="+str(polje +(pol)))
                        self.provjeri_polje_iza(fig,boja_nove_fig,pol,polje)

    def provjeri_polje_iza(self,fig,boja_nove_fig,polje,staro_polje):
        """ if fig.boja==boja_nove_fig:
            if self.tabla.polozaji[polje]==0:
                moguca_polja.append(polje)
        elif fig.boja!=boja_nove_fig:
            if  self.tabla.polozaji[polje]==0:
                moguce_polja.append(polje)
                #TREBA DODATI BRISANJE FIGURA
         """
        if  self.tabla.polozaji[polje]==0:
            self.moguca_polja[polje]=self.tabla.polozaji[staro_polje]
    
    def provjeri_dijagonale_kralja(self,fig,i,pravac):
        if (i//4)%2==0:
            if i%4!=0:
                self.provjeri_kralja_linijski(fig,i,pravac,-1)  #lijevo
            self.provjeri_kralja_linijski(fig,i,pravac,0)       #desno
        else:
            if i%4!=3:
                self.provjeri_kralja_linijski(fig,i,pravac,1)   #desno
            self.provjeri_kralja_linijski(fig,i,pravac,0)       #lijevo

    def provjeri_kralja_linijski(self,fig,i,pravac,bocno):
        trenutno=i
        #bira na koju stranu ide i tako ide do kraja
        smer_desno=True
        if (i//4)%2==0 and bocno==-1:
            smer_desno=False
        elif (i//4)%2==1 and bocno==0:
            smer_desno=False

        prvi_korak=True
        while True:
            if (trenutno//4)%2==0:  #Parni red
                if not smer_desno and trenutno%4==0:
                    #ako ide lijevo i kol=0 ispasce sa table 
                    break
                if smer_desno:
                    polje=trenutno+(pravac*4)
                    #ide desno u parnom redu, ostaje u istoj koloni  
                else:
                    polje=trenutno+(pravac*4)-1
                    #ide lijevo u parnom redu, mijenja kolonu
            else:   #Neparni red
                if smer_desno and trenutno%4==3:
                    break
                if smer_desno:
                    polje=trenutno+(pravac*4)+1  
                else:
                    polje=trenutno+(pravac*4)

            if not (0<=polje<=31):
                break

            if self.tabla.polozaji[polje]==0:
                #ako je prazno polje moze stati
                self.moguca_polja[polje]=0
            else:
                if prvi_korak:
                    #ako odma do sebe ima figuru protivnika
                    if fig.boja!=self.tabla.polozaji[polje].boja:
                        #racuna gdje je polje iza protivnika
                        if (polje//4)%2==0:
                            #protivnik u parnom redu
                            if not smer_desno and polje%4==0:
                                break
                            if smer_desno:
                                polje_iza=polje+(pravac*4)
                            else:
                                polje_iza=polje+(pravac*4)-1
                        else:
                            #protivnik u neparnom redu
                            if smer_desno and polje%4==3:
                                break
                            polje_iza=polje+(pravac*4)+1 if smer_desno else polje+(pravac*4)

                        if 0<=polje_iza<=31:
                            if self.tabla.polozaji[polje_iza]==0:
                                self.moguca_polja[polje_iza]=self.tabla.polozaji[polje]
                break
            #uzima novo polje da vidi da li moze jos iza njega da se krece
            trenutno=polje
            prvi_korak=False

    def nacrtaj_biranje_moci(self):
        # 3. Kreiramo pravougaonik za popup
        popup_pravougaonik=pygame.Rect(POPUP_RAZMAK_SIR,POPUP_RAZMAK_VIS,POPUP_SIR,POPUP_VIS)
        
        # 4. Crta se unutrašnjost (SIVA pozadina)
        pygame.draw.rect(self.proz,SIVA,popup_pravougaonik)
        
        # 5. Crta se ivica (CRNA boja, debljina ivice 4 piksela)
        pygame.draw.rect(self.proz,CRNA,popup_pravougaonik,4)
        
        # 6. Renderujemo tekst koristeći tvoj FONT i BIJELA slova
        tekst_povrsina=FONT.render("Izaberite moc",True,BIJELA)
        
        # 7. Računamo poziciju teksta tako da bude tačno u centru našeg popup-a
        tekst_POPUP_RAZMAK_SIR=POPUP_RAZMAK_SIR+(POPUP_SIR-tekst_povrsina.get_width())//2
        tekst_POPUP_RAZMAK_VIS=POPUP_RAZMAK_VIS+15  # Pomjereno malo gore da ne udara u slike
        
        broj_moc1=self.dek_moci.vidi_prvi()
        broj_moc2=self.dek_moci.vidi_zadnji()
        slike_moci={
                1: TOPUZ_PLAVA,
                2: KRALJ_PLAVA,
                3: KONJ_PLAVI,
                4: STIT_PLAVA,
                5: OCI_PLAVI
            }
        slika1=slike_moci.get(broj_moc1,None)
        slika2=slike_moci.get(broj_moc2,None)
        # Crtanje ivica oko lijevog i desnog dugmeta (da se vizuelno odvoje)
        pygame.draw.rect(self.proz,CRNA,pygame.Rect(LIJEVO_POPUP_X,LIJEVO_POPUP_Y,DUGME_SIR_POPUP,DUGME_VIS_POPUP),2)
        pygame.draw.rect(self.proz,CRNA,pygame.Rect(DESNO_POPUP_X,DESNO_POPUP_Y,DUGME_SIR_POPUP,DUGME_VIS_POPUP),2)
        
        self.proz.blit(tekst_povrsina,(tekst_POPUP_RAZMAK_SIR,tekst_POPUP_RAZMAK_VIS))
        # 8. Računanje centra i crtanje slika unutar dugmića
        if slika1:
            slika1_x=LIJEVO_POPUP_X+(DUGME_SIR_POPUP-SLIKA)//2
            slika1_y=LIJEVO_POPUP_Y+(DUGME_VIS_POPUP-SLIKA)//2
            self.proz.blit(slika1,(slika1_x,slika1_y))
            
        if slika2:
            slika2_x=DESNO_POPUP_X+(DUGME_SIR_POPUP-SLIKA)//2
            slika2_y=DESNO_POPUP_Y+(DUGME_VIS_POPUP-SLIKA)//2
            self.proz.blit(slika2,(slika2_x,slika2_y))
        
        # 9. Ažuriramo ekran da bi se promene odmah videle
        pygame.display.update()
        
    def dobij_stranu_moci_od_misa(self,poz):
        x_mis,y_mis=poz
        
        # 1. Proveravamo da li je klik unutar LIJEVOG dela popup-a (Moć 1)
        if LIJEVO_POPUP_X<=x_mis<=LIJEVO_POPUP_X+DUGME_SIR_POPUP and LIJEVO_POPUP_Y<=y_mis<=LIJEVO_POPUP_Y+DUGME_VIS_POPUP:
            return 1
            
        # 2. Proveravamo da li je klik unutar DESNOG dela popup-a (Moć 2)
        elif DESNO_POPUP_X<=x_mis<=DESNO_POPUP_X+DUGME_SIR_POPUP and DESNO_POPUP_Y<=y_mis<=DESNO_POPUP_Y+DUGME_VIS_POPUP:
            return 2
            
        # 3. Ako je kliknuto van oba dela
        else:
            return -1
    def dodjeli_moc(self, izabrano):
        if izabrano!=-1:#ako smo izabrali neku moc
                print("\tizabrana moc "+str(izabrano))
                self.biranje=False
                print("\tbiranje "+str(self.biranje))

                if izabrano==1:
                    #skini sa deka na mjestu polozaja
                    moc=self.dek_moci.ukloni_prvi()
                else:
                    moc=self.dek_moci.ukloni_zadnji()
                #self.tren=Figura()
                if moc==1:
                    print("\t1-topuz")
                    self.tren.postavi_topuz()
                elif moc==2:
                    print("\t2-krunisanje")
                    self.tren.krunisi()
                elif moc==3:
                    print("\t3-sarac")
                    self.tren.postavi_sarca()
                elif moc==4:
                    print("\t4-oklop")
                    self.tren.postavi_oklop()
                elif moc==5:
                    print("\t4-pogled")
                    self.tren.postavi_pogled()
                #obrisi popup
                self.tabla.nacrtaj(self.proz)
                pygame.display.update()
def promadji_najblizu(tren,polozaji):
    najbliza_fig=None
    najmanja_dist=float('inf')
    for fig in polozaji:
        if fig!=0 and fig.boja!=tren.boja:
            x,y=fig.x,fig.y
            dist=((x-tren.x)**2)+((y-tren.y)**2)

            if dist<najmanja_dist:
                najmanja_dist=dist
                najbliza_fig=fig
    if najbliza_fig:
        najbliza_fig.zaledjena=2
        tren.oko=False
        print("Zamznuta fig na indeksu:"+str(najbliza_fig.indeks))
            