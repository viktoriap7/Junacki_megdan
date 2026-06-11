import time
from copy import deepcopy
from protivnik.zhash import Zobrist_hash
from dama.figura import Figura
from dama.const import *
from dama.igra import Igra
from dama.strukture import Dek
class Racun:
    def __init__(self,igra):
        self.igra=igra
        self.zhash=Zobrist_hash()

        self.traspoziciona_tabla={}
        self.max_t_tabla=500000

        self.poc_vrijeme=0
        self.duzina_razmisljanja=3
    def heuristika_izracunaj(self,polozaji):
        ocjena=0
        for fig in polozaji:
            if fig!=0:
                zbir=0
                if 0<fig.indeks%4<3:
                    zbir+=10
                if fig.marko:
                    zbir+=20
                if fig.kralj:
                    zbir+=50
                if fig.topuz:
                    zbir+=30
                if fig.sarac:
                    zbir+=20
                if fig.oklop:
                    zbir+=10
                if fig.oklop_brojac>0:
                    zbir+=20
                if fig.obrve:
                    zbir+=20
                if fig.zaledjena:
                    zbir-=20

                if fig.boja==CRVENA:
                    ocjena+=zbir
                else:
                    ocjena-=zbir
        return ocjena
    def dobij_sve_poteze(self,polozaji,na_redu,tren):
        """ format poteza(pocetni indeks fig, krajnji indeks fig, indeks pojedene fig)
         ako nista nije pojedeno vraca None,
          upisuje sve korake u moguci_potezi igre """
        #tren je ako je izabrana figura koja se mora kretati
        simulacija=Igra(None)
        simulacija.tabla.polozaji=polozaji
        simulacija.na_redu=na_redu
        svi_potezi=[]
        if tren:
            simulacija.tren=polozaji[tren]
            svi_potezi=simulacija.dobij_korake_koji_jedu()
        else:
            for indeks,fig in enumerate(polozaji):
                if fig !=0 and fig.boja==na_redu:
                    simulacija.tren=fig
                    simulacija.dobij_moguce_korake()
                    for novi_indeks,jede_fig in simulacija.moguca_polja.items():
                        if jede_fig==0:
                            jede_indeks=None
                        else:
                            jede_indeks=jede_fig.indeks
                        svi_potezi.append((indeks,novi_indeks,jede_indeks))
        return svi_potezi

    def pomjeri(self,stari_polozaji,potez):
        """ vraca novu tablu na kojoj je izvrsen ovaj pokret 
        i da li je pojedeno nesto """
        polozaji=deepcopy(stari_polozaji)
        pojeo=False
        tren=None
        stari_indeks,novi_indeks,index_jede_fig=potez
        fig=polozaji[stari_indeks]
        if index_jede_fig:
            if fig.topuz_brojac > 0:
                fig.topuz_brojac -= 1
            polozaji[index_jede_fig]=0
            pojeo=True

        polozaji[novi_indeks]=fig 
        polozaji[stari_indeks]=0
        fig.indeks=novi_indeks
        if pojeo:
            tren=novi_indeks
        return polozaji,tren

    def minmax(self,polozaji,tren,dubina,alfa,beta,na_redu):
        vrijeme=time.time()-self.poc_vrijeme
        print("vrijeme: "+str(vrijeme))
        if vrijeme>self.duzina_razmisljanja:
            return self.heuristika_izracunaj(polozaji)

        if dubina==0:
            return self.heuristika_izracunaj(polozaji)

        if na_redu==CRVENA: #MAX
            max_ocjena=float('-inf')
            
            svi_potezi=self.dobij_sve_poteze(polozaji,na_redu,tren)

            if not svi_potezi:
                return self.heuristika_izracunaj(polozaji)
            for potez in svi_potezi:
                sledeci_na_redu=CRVENA
                novi_polozaji,novi_tren=self.pomjeri(polozaji,potez)
                if novi_tren==None:
                    sledeci_na_redu=PLAVA
                ocjena=self.minmax(novi_polozaji,novi_tren,dubina-1,alfa,beta,sledeci_na_redu)
                max_ocjena=max(ocjena,max_ocjena)
                alfa = max(alfa, max_ocjena)
                if beta <= alfa:
                    break
            return max_ocjena
        else:   #MIN
            min_ocjena=float('inf')
            
            svi_potezi=self.dobij_sve_poteze(polozaji,na_redu,tren)
            
            if not svi_potezi:
                return self.heuristika_izracunaj(polozaji)
            for potez in svi_potezi:
                sledeci_na_redu=PLAVA
                novi_polozaji,novi_tren=self.pomjeri(polozaji,potez)
                if novi_tren==None:
                    sledeci_na_redu=CRVENA
                ocjena=self.minmax(novi_polozaji,novi_tren,dubina-1,alfa,beta,sledeci_na_redu)
                min_ocjena=min(ocjena,min_ocjena)
                beta = min(beta, min_ocjena)
                if beta <= alfa:
                    break
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
                novi_polozaji,novi_tren=self.pomjeri(self.igra.tabla.polozaji,potez)
                if novi_tren==None:
                    sledeci_na_redu=PLAVA
                ocjena = self.minmax(novi_polozaji, novi_tren, dubina, float('-inf'), float('inf'), sledeci_na_redu)
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
        stari_indeks,novi_indeks,tren=self.pronadji_najbolji_potez()
        self.igra.tren=self.igra.tabla.polozaji[stari_indeks]
        self.igra.dobij_moguce_korake()
        print("nasao potez")
        self.igra.pokusaj_pomjeriti(novi_indeks)
        if self.igra.biranje:
            moc=self.igra.dek_moci.ukloni_prvi()
            self.igra.tren.dodjeli_moc(moc)
            self.igra.biranje=False
            self.igra.upravljaj_redom()

