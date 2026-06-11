import time
from protivnik.zhash import Zobrist_hash
from dama.figura import Figura
from dama.const import *
from dama.igra import Igra
from dama.strukture import Dek
class Racun:
    def __init__(self,igra,zhash):
        self.igra=igra
        self.zhash=zhash

        self.traspoziciona_tabla={}
        self.max_t_tabla=500000

        self.poc_vrijeme=0
        self.duzina_razmisljanja=3
    
    def zapisi_u_t_tabeli(self,tren_hash,tren_dubina,ocjena):
        pass
    def heuristika_izracunaj(self,polozaji):
        ocjena=0
        for fig in polozaji:
            if fig!=0:
                zbir=0
                if fig.marko:
                    zbir+=2
                if fig.kralj:
                    zbir+=5
                if fig.topuz:
                    zbir+=3
                if fig.sarac:
                    zbir+=2
                if fig.oklop:
                    zbir+=1
                if fig.oklop_brojac>0:
                    zbir+=2
                if fig.obrve:
                    zbir+=2
                if fig.zaledjena:
                    zbir-=2

                if fig.boja==CRVENA:
                    ocjena+=zbir
                else:
                    ocjena-=zbir
        return ocjena
    def pronadji_najbolji_potez(self,tren_tabla):
        self.poc_vrijeme=time.time()
        na_redu=CRVENA

        if self.igra.lanac:
            svi_potezi=self.igra.dobij_korake_koji_jedu()
        else:
            svi_potezi=self.dobij_sve_poteze(tren_tabla.polozaji,na_redu)
        if not svi_potezi:
            #ako nema mogucih poteza
            return None
        tren_dubina=1
        najbolji_potez=svi_potezi[0]
        naj_potez=None
        while True:
            vrijeme_isteklo=False
            if time.time()-self.poc_vrijeme>=self.duzina_razmisljanja-0.15:
                break
            naj_ocjena=float('-inf')
            naj_potez=None

            for potez in svi_potezi:
                #ubacuje u provjeru pojedinacan potez
                ocjena=self.grana_minimax(tren_tabla.polozaji,tren_dubina,float('-inf'),float('inf'),na_redu,potez)
                if time.time()-self.poc_vrijeme>=self.duzina_razmisljanja-0.15:
                    vrijeme_isteklo=True
                    break
                if ocjena>naj_ocjena:
                    naj_ocjena=ocjena
                    naj_potez=potez
            if vrijeme_isteklo:
                break
            if naj_potez:
                najbolji_potez=naj_potez
            tren_dubina+=1
        #upisati moguca polja u igru kako bi mogli pokrenuti pokusaj pomjeriti
        stari_indeks,novi_indeks,jede_fig=najbolji_potez
        self.igra.moguca_polja={}
        self.igra.moguca_polja[novi_indeks]=jede_fig
        self.igra.tren=tren_tabla.polozaji[stari_indeks]
        return novi_indeks
                

    def igraj(self):
        #self.igra=Igra()
        novi_indeks=self.pronadji_najbolji_potez(self.igra.tabla)
        self.igra.pokusaj_pomjeriti(novi_indeks)
        if self.igra.biranje:
            moc=self.igra.dek_moci.ukloni_prvi()
            self.igra.tren.dodjeli_moc(moc)
            self.igra.biranje=False
            self.igra.upravljaj_redom()


    def dobij_sve_poteze(self,polozaji,na_redu):
        svi_potezi=[]
        for polje in range(32):
            if polozaji[polje]!=0:
                if polozaji[polje].boja==na_redu:    
                    #self.igra=Igra()
                    self.igra.tren=polozaji[polje]
                    self.igra.dobij_moguce_korake()
                    for indeks in self.igra.moguca_polja:
                        svi_potezi.append((polje,indeks,self.igra.moguca_polja[indeks]))
        return svi_potezi

        
    def minimax(self,polozaji,dubina,alfa,beta,na_redu,indeks_fig_lanac=None):


        #gledamo da li smo vec racunali ovo stanje tabele
        tren_hash=self.traspoziciona_tabla.izracunaj(polozaji,na_redu)
        if tren_hash in self.traspoziciona_tabla:
            sacuvana_dubina,sacuvana_ocjena=self.traspoziciona_tabla[tren_hash]
            #ako smo bolje izracunali nekad prije, vrati tu ocjenu
            if sacuvana_dubina>=dubina:
                return sacuvana_ocjena   
            
        if dubina==0:
            return self.heuristika_izracunaj(polozaji)

        if indeks_fig_lanac:
            svi_potezi=self.dobij_sta_fig_moze_pojesti(polozaji,na_redu)
        else:
            svi_potezi=self.dobij_sve_poteze(polozaji,na_redu)
        
        #ako nema sta da se odigra
        if not svi_potezi: 
            #obrni na redu kada se lanac zavrsi
            if indeks_fig_lanac:
                if na_redu==CRVENA:
                    sledeci_na_redu=PLAVA
                else:
                    sledeci_na_redu=CRVENA
                return self.minimax(polozaji,dubina,alfa,beta,sledeci_na_redu)
            else:
                return self.heuristika_izracunaj(polozaji)


        if na_redu==CRVENA: #max
            max_ocjena=float('-inf')
            
            
            for potez in svi_potezi:
                ocjena=self.grana_minimax(polozaji,dubina,alfa,beta,CRVENA,potez)
                max_ocjena=max(max_ocjena,ocjena)
                alfa=max(max_ocjena,alfa)
                if beta<=alfa:
                    break
            self.traspoziciona_tabla[tren_hash]=(dubina,max_ocjena)
            return max_ocjena
        else: #min
            min_ocjena=float('inf')
            for potez in svi_potezi:
                ocjena=self.grana_minimax(polozaji,dubina,alfa,beta,PLAVA,potez)
                min_ocjena=min(min_ocjena,ocjena)
                beta=min(beta,min_ocjena)
                if beta<=alfa:
                    break
            self.traspoziciona_tabla[tren_hash]=(dubina,min_ocjena)
            return min_ocjena
                
                
    def grana_minimax(self,polozaji,dubina,alfa,beta,na_redu,potez):                
        fig_indeks,novi_indeks,jede_fig=potez
        fig=polozaji[fig_indeks]
        pojedena_fig=None

        if jede_fig!=0:
            pojedena_fig=jede_fig
            polozaji[jede_fig.indeks]=0
        polozaji[novi_indeks]=fig
        polozaji[fig_indeks]=0
        
        stao_oranje=novi_indeks in self.igra.tabla.oranje
        if stao_oranje:
            stari_topuz=fig.topuz
            stari_sarac=fig.sarac
            stari_oklop=fig.oklop
            stari_obrve=fig.obrve
            stari_kralj=fig.kralj
            stari_marko=fig.marko
            
            dek=self.igra.dek_moci
            prva_moc=dek.vidi_prvi()
            
            fig.dodjeli_moc(prva_moc)
            ocjena=self.lanac_minimax(polozaji,dubina,alfa,beta,na_redu,jede_fig,novi_indeks)
            fig.topuz,fig.kralj,fig.sarac=stari_topuz,stari_kralj,stari_sarac
            fig.oklop,fig.obrve,fig.marko =stari_oklop,stari_obrve,stari_marko
            """ 
            zadnja_moc=dek.vidi_zadnji()
            
            fig.dodjeli_moc(zadnja_moc)
            ocjena_zadnja=self.lanac_minimax(polozaji,dubina,alfa,beta,na_redu,jede_fig,novi_indeks)
            fig.topuz,fig.kralj,fig.sarac=stari_topuz,stari_kralj,stari_sarac
            fig.oklop,fig.obrve,fig.marko =stari_oklop,stari_obrve,stari_marko
             """
            """
             if na_redu==CRVENA:
                if ocjena_prva>ocjena_zadnja:
                    fig.dodjeli_moc(prva_moc)
                    ocjena=ocjena_prva
                else:
                    fig.dodjeli_moc(zadnja_moc)
                    ocjena=ocjena_zadnja
            else:
                if ocjena_prva<ocjena_zadnja:
                    fig.dodjeli_moc(prva_moc)
                    ocjena=ocjena_prva
                else:
                    fig.dodjeli_moc(zadnja_moc)
                    ocjena=ocjena_zadnja """
        else:
            ocjena=self.lanac_minimax(polozaji,dubina,alfa,beta,na_redu,jede_fig,novi_indeks)
        if stao_oranje:
            fig.topuz,fig.kralj,fig.sarac=stari_topuz,stari_kralj,stari_sarac
            fig.oklop,fig.obrve,fig.marko =stari_oklop,stari_obrve,stari_marko
            
        polozaji[fig_indeks]=fig
        polozaji[novi_indeks]=0
        if jede_fig!=0:
            polozaji[jede_fig.indeks]=pojedena_fig
        
        return ocjena
    def lanac_minimax(self, polozaji,dubina,alfa,beta,na_redu,jede_fig,novi_indeks):
        
        if jede_fig!=0:
            ocjena=self.minimax(polozaji,dubina,alfa,beta,na_redu,novi_indeks)
        else:
            if na_redu==CRVENA:
                sledeci_na_redu=PLAVA
            else:
                sledeci_na_redu=CRVENA
            ocjena=self.minimax(polozaji,dubina-1,alfa,beta,sledeci_na_redu)
        