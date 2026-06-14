import random
import time
import os
from copy import deepcopy
from protivnik.zhash import Zobrist_hash
from dama.figura import Figura
from dama.const import *
from dama.igra import Igra,promadji_najblizu
from dama.strukture import Dek
class Racun:
    def __init__(self,igra):
        self.igra=igra
        self.zhash=Zobrist_hash()

        self.ime_fajla="t_tabela.txt"
        self.traspoziciona_tabla=self.ucitaj_iz_fajla()
        self.max_t_tabela=50000
        self.poc_vrijeme=0
        self.duzina_razmisljanja=90
    def sacuvaj_u_tabelu(self, h, ocjena, dubina):
        
        if len(self.traspoziciona_tabla) >= self.max_t_tabla:
            svi_kljucevi = list(self.traspoziciona_tabla.keys())
            kljuc_za_brisanje = random.choice(svi_kljucevi)
            del self.traspoziciona_tabla[kljuc_za_brisanje]
        
        self.traspoziciona_tabla[h] = (ocjena, dubina)
    def ucitaj_iz_fajla(self):
        tabela = {}
        if os.path.exists(self.ime_fajla):
            with open(self.ime_fajla, 'r') as f:
                for red in f:
                    h, score, depth = red.strip().split(',')
                    tabela[int(h)] = (int(score), int(depth))
        print("ucitano")
        return tabela
    def upisi_u_fajl(self):
        with open(self.ime_fajla, 'w') as f:
            for h, podaci in self.traspoziciona_tabla.items():
                score, depth = podaci
                # Upisujemo u formatu "hash,score,depth"
                f.write(f"{h},{score},{depth}\n")
        print("zapisano")
    def heuristika_izracunaj(self,polozaji):
        ocjena=0
        for fig in polozaji:
            if fig!=0:
                zbir=100
                if fig.indeks//4==0:
                    zbir+=3
                if 0<fig.indeks%4<3:
                    zbir+=3
                if fig.marko:
                    zbir+=20
                if fig.kralj:
                    zbir+=70
                if fig.topuz:
                    zbir+=30
                if fig.sarac:
                    zbir+=20
                if fig.oklop:
                    zbir+=10
                if fig.oklop_brojac>0:
                    zbir+=5
                if fig.obrve:
                    zbir+=20
                if fig.zaledjena:
                    zbir-=5

                if fig.boja==CRVENA:
                    ocjena+=zbir
                else:
                    ocjena-=zbir
        return ocjena
    def dobij_sve_poteze(self,polozaji,na_redu,tren):
        """ format poteza(pocetni indeks fig, krajnji indeks fig, indeks pojedene fig,moc)
         ako nista nije pojedeno vraca None,
          upisuje sve korake u moguci_potezi igre """
        #tren je ako je izabrana figura koja se mora kretati
        simulacija=Igra(None)
        simulacija.tabla.polozaji=deepcopy(polozaji)
        simulacija.na_redu=deepcopy(na_redu)
        svi_potezi=[]
        if tren:    #dio za lanac
            simulacija.tren=polozaji[tren]
            svi_potezi=simulacija.dobij_korake_koji_jedu()
        else:       #dio za obican potez
            for indeks,fig in enumerate(polozaji):
                if fig !=0 and fig.boja==na_redu:
                    simulacija.tren=fig
                    simulacija.dobij_moguce_korake()
                    for novi_indeks,jede_fig in simulacija.moguca_polja.items():
                        if jede_fig==0:
                            jede_indeks=None
                        else:
                            jede_indeks=jede_fig.indeks
                        svi_potezi.append((indeks,novi_indeks,jede_indeks,None))
                    if fig.obrve==True:
                        svi_potezi.append((indeks,indeks,None,5))
                    if fig.oklop==True:
                        svi_potezi.append((indeks,indeks,None,4))
        return svi_potezi

    def pomjeri(self,stari_polozaji,potez,dek):
        """ vraca novu tablu na kojoj je izvrsen ovaj pokret 
        i da li je pojedeno nesto """
        polozaji=deepcopy(stari_polozaji)
        dek_moci=deepcopy(dek)
        pojeo=False
        tren=None
        stari_indeks,novi_indeks,index_jede_fig,moc=potez
        fig=polozaji[stari_indeks]
        if moc:
            if moc==4:
                fig.upotrebi_oklop()
            elif moc==5:
                promadji_najblizu(fig,polozaji)
        else:    
            if index_jede_fig:
                if fig.topuz_brojac > 0:
                    fig.topuz_brojac -= 1
                polozaji[index_jede_fig]=0
                pojeo=True

            polozaji[novi_indeks]=fig 
            polozaji[stari_indeks]=0
            fig.indeks=novi_indeks
            if novi_indeks in self.igra.tabla.oranje:
                moc=dek_moci.ukloni_prvi()
                fig.dodjeli_moc(moc)
            if pojeo:
                tren=novi_indeks
        return polozaji,tren,dek

    def minmax(self,polozaji,tren,dubina,alfa,beta,na_redu,dek):
        vrijeme=time.time()-self.poc_vrijeme
        print("vrijeme: "+str(vrijeme))
        if vrijeme>self.duzina_razmisljanja:
            return self.heuristika_izracunaj(polozaji)

        if dubina==0:
            return self.heuristika_izracunaj(polozaji)
        h = self.zhash.izracunaj(polozaji, na_redu)
        rezultat = self.traspoziciona_tabla.get(h)
        if rezultat:
            ocjena, d = rezultat 
            if d >= dubina:  
                return ocjena
        if na_redu==CRVENA: #MAX
            max_ocjena=float('-inf')
            
            svi_potezi=self.dobij_sve_poteze(polozaji,na_redu,tren)

            if not svi_potezi:
                return self.heuristika_izracunaj(polozaji)
            for potez in svi_potezi:
                sledeci_na_redu=CRVENA
                novi_polozaji,novi_tren,novi_dek=self.pomjeri(polozaji,potez,dek)
                if novi_tren==None:
                    sledeci_na_redu=PLAVA
                ocjena=self.minmax(novi_polozaji,novi_tren,dubina-1,alfa,beta,sledeci_na_redu,novi_dek)
                max_ocjena=max(ocjena,max_ocjena)
                alfa = max(alfa, max_ocjena)
                if beta <= alfa:
                    break
            self.traspoziciona_tabla[h] = (max_ocjena,dubina)
            return max_ocjena
        else:   #MIN
            min_ocjena=float('inf')
            
            svi_potezi=self.dobij_sve_poteze(polozaji,na_redu,tren)
            
            if not svi_potezi:
                return self.heuristika_izracunaj(polozaji)
            for potez in svi_potezi:
                sledeci_na_redu=PLAVA
                novi_polozaji,novi_tren,novi_dek=self.pomjeri(polozaji,potez,dek)
                if novi_tren==None:
                    sledeci_na_redu=CRVENA
                ocjena=self.minmax(novi_polozaji,novi_tren,dubina-1,alfa,beta,sledeci_na_redu,novi_dek)
                min_ocjena=min(ocjena,min_ocjena)
                beta = min(beta, min_ocjena)
                if beta <= alfa:
                    break
            self.traspoziciona_tabla[h]=(min_ocjena,dubina)
            return min_ocjena
    def pronadji_najbolji_potez(self):
        #koristi izabranu figuru da vidi da li je lanac
        self.poc_vrijeme=time.time()
        tren = self.igra.tren.indeks if self.igra.tren else None
        svi_potezi=self.dobij_sve_poteze(self.igra.tabla.polozaji,CRVENA,tren)
        najbolji_potez=svi_potezi[0]
        dubina=1

        while True:
            print("dubina "+str(dubina))
            max_ocjena=float('-inf')
            temp_najbolji = None
            if time.time()-self.poc_vrijeme>self.duzina_razmisljanja:
                break
            for potez in svi_potezi:
                sledeci_na_redu=CRVENA
                novi_polozaji,novi_tren,novi_dek=self.pomjeri(self.igra.tabla.polozaji,potez,self.igra.dek_moci)
                if novi_tren==None:
                    sledeci_na_redu=PLAVA
                ocjena = self.minmax(novi_polozaji, novi_tren, dubina, float('-inf'), float('inf'), sledeci_na_redu,novi_dek)
                print("ocjena: "+str(ocjena)+" za potez "+str(potez))
                if ocjena>max_ocjena:
                    max_ocjena=ocjena
                    temp_najbolji=potez
            if temp_najbolji:
                najbolji_potez=temp_najbolji
            dubina+=1
        return najbolji_potez
    
    def igraj(self):
        print("bira racunar")
        #self.igra=Igra()
        stari_indeks,novi_indeks,tren,moc=self.pronadji_najbolji_potez()
        self.igra.tren=self.igra.tabla.polozaji[stari_indeks]
        if moc:
            if moc==4:
                self.igra.tren.upotrebi_oklop()
                print("odigrao oklop")
            elif moc==5:
                promadji_najblizu(self.igra.tren,self.igra.tabla.polozaji)
                print("odigrao pogled")
            self.igra.upravljaj_redom()
        else:    
            self.igra.dobij_moguce_korake()
            print("nasao potez")
            self.igra.pokusaj_pomjeriti(novi_indeks)
            if self.igra.biranje:
                moc=self.igra.dek_moci.ukloni_prvi()
                self.igra.tren.dodjeli_moc(moc)
                self.igra.biranje=False
                self.igra.upravljaj_redom()

    def ispitaj_trajanje(self):
        """ vraca ko pobjedjuje, none igra se nastavlja, za remi vrati crnu boju """
        
        if self.igra.tabla.bijele_fig==0:
            return CRVENA
        if self.igra.tabla.crne_fig==0:
            return PLAVA
        svi_potezi=self.dobij_sve_poteze(self.igra.tabla.polozaji,self.igra.na_redu,None)
        if svi_potezi==[]:
            if self.igra.na_redu==PLAVA:
                return CRVENA
            else:
                return PLAVA
        if self.igra.broj_poteza>40:
            return CRNA
        return None

