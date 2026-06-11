import random
from dama.const import *
from dama.figura import Figura
class Zobrist_hash:
    def __init__(self):
        random.seed(10)
        self.na_redu_protivnik=random.getrandbits(64)
        self.tabla_kretanja_figura={}
        self.tabla_topuza={}
        self.tabla_sarca={}
        self.tabla_oklopa={}
        self.tabla_koristi_oklop={}
        self.tabla_pogleda={}
        self.tabla_zaledjena={}
        for indeks in range(32):
            self.tabla_kretanja_figura[indeks]={
                1:random.getrandbits(64),
                2:random.getrandbits(64),
                3:random.getrandbits(64),
                4:random.getrandbits(64)
            }
            self.tabla_topuza[indeks]=random.getrandbits(64)
            self.tabla_sarca[indeks]=random.getrandbits(64)
            self.tabla_oklopa[indeks]=random.getrandbits(64)
            self.tabla_koristi_oklop[indeks]=random.getrandbits(64)
            self.tabla_pogleda[indeks]=random.getrandbits(64)
            self.tabla_zaledjena[indeks]=random.getrandbits(64)            
    def izracunaj(self,polozaji,na_redu):
        tren_hash=0
        
        for indeks,fig in enumerate(polozaji):
            
            if fig!=0:
                if fig.boja==PLAVA:
                    vrednost_fig=1
                else:
                    vrednost_fig=3
                if fig.kralj:
                    vrednost_fig+=1
            tren_hash^=self.tabla_kretanja_figura[indeks][vrednost_fig]
            if fig.topuz:
                tren_hash^=self.tabla_topuza[indeks]
            if fig.sarac:
                tren_hash^=self.tabla_sarca[indeks]
            if fig.oklop:
                tren_hash^=self.tabla_oklopa[indeks]
            if fig.oklop_brojac>0:
                tren_hash^=self.tabla_koristi_oklop[indeks]
            if fig.obrve:
                tren_hash^=self.tabla_pogleda[indeks]
            if fig.zaledjena:
                tren_hash^=self.tabla_zaledjena[indeks]
        if na_redu==CRVENA:
            tren_hash^=self.na_redu_protivnik
        return tren_hash