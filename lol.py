import copy
import time
import random

class GameState:
    """ 
    Podloga za Undo sistem. Pravi brzu kopiju trenutnog stanja table 
    kako bi Minimax mogao da simulira poteze i vrati ih unazad.
    """
    def __init__(self, polozaji, na_redu, lanac, trenutni_indeks=None):
        self.polozaji = copy.deepcopy(polozaji)
        self.na_redu = na_redu
        self.lanac = lanac
        self.trenutni_indeks = trenutni_indeks


class ZobristHash:
    """
    Otisak prsta za svaku poziciju na tabli. 
    Garantuje unikatne 64-bitne brojeve za svaku kombinaciju figura.
    """
    def __init__(self):
        # Fiksni seed osigurava da su brojevi isti u svakoj partiji (omogućava analitiku)
        random.seed(42)
        
        # Generisanje unikatnih brojeva za svih 32 polja i 4 moguća stanja figure
        # 1: plava obična, 2: plava kralj, 3: crvena obična, 4: crvena kralj
        self.tabla_brojeva = {}
        for polje in range(32):
            self.tabla_brojeva[polje] = {
                1: random.getrandbits(64),
                2: random.getrandbits(64),
                3: random.getrandbits(64),
                4: random.getrandbits(64)
            }
        # Broj koji XOR-ujemo kada je Crveni (AI) na potezu
        self.na_redu_crveni = random.getrandbits(64)

    def izracunaj_hash(self, polozaji, na_redu):
        trenutni_hash = 0
        for indeks, fig in enumerate(polozaji):
            if fig != 0:
                # Određivanje stanja na osnovu boje i titule kralja
                stanje = 1 if fig.boja == "PLAVA" else 3
                if fig.kralj:
                    stanje += 1
                
                # Primena XOR operacije za mešanje bitova
                trenutni_hash ^= self.tabla_brojeva[indeks][stanje]
                
        if na_redu == "CRVENA":
            trenutni_hash ^= self.na_redu_crveni
            
        return trenutni_hash


class VjestackaInteligencija:
    """
    Glavni AI algoritam. Sadrži Minimax, Alpha-Beta odsecanje, 
    Iterative Deepening i pametnu Strategiju Zamene u tabeli.
    """
    def __init__(self, igra_objekat):
        self.igra = igra_objekat
        self.zobrist = ZobristHash()
        
        # Transpoziciona tabela i njena ograničenja (oko 50 MB RAM-a)
        self.transpoziciona_tabela = {}
        self.max_velicina_tabele = 500000
        
        # Kontrola vremena (Strogo ograničenje od 3 sekunde)
        self.vreme_pocetka = 0
        self.vremenski_limit = 3.0

    def upisi_u_transpozicionu_tabelu(self, trenutni_hash, dubina, evaluacija):
        """ Implementacija Strategije Zamene (Izbacivanje najpliće pozicije) """
        # 1. Ako pozicija postoji, prepisujemo je samo ako je nova pretraga išla DUBLJE
        if trenutni_hash in self.transpoziciona_tabela:
            stara_dubina, _ = self.transpoziciona_tabela[trenutni_hash]
            if dubina >= stara_dubina:
                self.transpoziciona_tabela[trenutni_hash] = (dubina, evaluacija)
                
        # 2. Ako ne postoji, a tabela ima mesta, samo je upisujemo
        elif len(self.transpoziciona_tabela) < self.max_velicina_tabele:
            self.transpoziciona_tabela[trenutni_hash] = (dubina, evaluacija)
            
        # 3. Ako je tabela PUNA, uzorkujemo 5 nasumičnih i izbacujemo najpliću
        else:
            nasumicni_kljucevi = random.sample(list(self.transpoziciona_tabela.keys()), 5)
            najgori_kljuc = nasumicni_kljucevi[0]
            najmanja_dubina, _ = self.transpoziciona_tabela[najgori_kljuc]
            
            for k in nasumicni_kljucevi:
                d, _ = self.transpoziciona_tabela[k]
                if d < najmanja_dubina:
                    najmanja_dubina = d
                    najgori_kljuc = k
            
            # Zamena mesta ako je naša trenutna pretraga dublja od najlošije u uzorku
            if dubina > najmanja_dubina:
                del self.transpoziciona_tabela[najgori_kljuc]
                self.transpoziciona_tabela[trenutni_hash] = (dubina, evaluacija)

    def heuristika_evaluacija(self, polozaji):
        """ Statička procena table (Crveni teži plusu, Plavi minusu) """
        skor = 0
        for fig in polozaji:
            if fig != 0:
                vrednost = 10 if not fig.kralj else 30
                
                # Uračunavanje modifikatora moći u ocenu pozicije
                if fig.zaledjena_brojac > 0:
                    vrednost -= 4
                if fig.oklop_brojac > 0:
                    vrednost += 2
                    
                if fig.boja == "CRVENA":
                    skor += vrednost
                else:
                    skor -= vrednost
        return skor

    def dobij_sve_moguce_poteze(self, tabla, boja, figura_u_lancu=None):
        """ 
        Vraća listu svih legalnih poteza: (od_polja, do_polja, sta_jede).
        Ako je aktiviran lanac, forsira kretanje SAMO aktivne figure.
        """
        potezi = []
        figure_za_proveru = [figura_u_lancu] if figura_u_lancu else tabla.polozaji
        
        for fig in figure_za_proveru:
            if fig != 0 and fig.boja == boja and fig.zaledjena_brojac == 0:
                # Privremeno mapiranje na logiku tvoje igre radi dobijanja koraka
                stari_tren = self.igra.tren
                self.igra.tren = fig
                self.igra.dobij_moguce_korake()
                
                for cilj, sta_jede in self.igra.moguca_polja.items():
                    potezi.append((fig.indeks, cilj, sta_jede))
                    
                self.igra.tren = stari_tren
        return potezi

    def minimax(self, trenutna_tabla, dubina, alpha, beta, na_redu, figura_u_lancu=None):
        # Hitna kočnica za vreme (Iterative Deepening zahtev)
        if time.time() - self.vreme_pocetka >= self.vremenski_limit - 0.2:
            return self.heuristika_evaluacija(trenutna_tabla.polozaji)

        # Optimizacija: Brzo čitanje iz Transpozicione tabele
        trenutni_hash = self.zobrist.izracunaj_hash(trenutna_tabla.polozaji, na_redu)
        if trenutni_hash in self.transpoziciona_tabela:
            smer_dubina, sacuvana_eval = self.transpoziciona_tabela[trenutni_hash]
            if smer_dubina >= dubina:
                return sacuvana_eval

        # Bazni slučaj (kraj pretrage po dubini)
        if dubina == 0:
            return self.heuristika_evaluacija(trenutna_tabla.polozaji)

        svi_potezi = self.dobij_sve_moguce_poteze(trenutna_tabla, na_redu, figura_u_lancu)
        if not svi_potezi:
            return self.heuristika_evaluacija(trenutna_tabla.polozaji)

        if na_redu == "CRVENA": # MAKSIMIZATOR (Računar / AI)
            max_eval = float('-inf')
            for od_p, do_p, sta_jede in svi_potezi:
                # Čuvanje stanja pre simulacije poteza (Undo korak)
                stari_okvir = GameState(trenutna_tabla.polozaji, na_redu, trenutna_tabla.lanac)
                
                potez_je_lanac = trenutna_tabla.izvrsi_simulirani_potez(od_p, do_p, sta_jede)
                
                # REŠENJE ZA LANAC: Ako je u lancu, isti igrač nastavlja pretragu na istoj dubini!
                if potez_je_lanac:
                    evaluacija = self.minimax(trenutna_tabla, dubina - 1, alpha, beta, "CRVENA", trenutna_tabla.polozaji[do_p])
                else:
                    evaluacija = self.minimax(trenutna_tabla, dubina - 1, alpha, beta, "PLAVA", None)
                
                # Vraćanje table unazad iz sačuvanog stanja
                trenutna_tabla.polozaji = stari_okvir.polozaji
                
                max_eval = max(max_eval, evaluacija)
                alpha = max(alpha, max_eval)
                if beta <= alpha: # Alpha-Beta odsecanje
                    break
            
            self.upisi_u_transpozicionu_tabelu(trenutni_hash, dubina, max_eval)
            return max_eval

        else: # MINIMIZATOR (Čovek / Plavi)
            min_eval = float('inf')
            for od_p, do_p, sta_jede in svi_potezi:
                stari_okvir = GameState(trenutna_tabla.polozaji, na_redu, trenutna_tabla.lanac)
                
                potez_je_lanac = trenutna_tabla.izvrsi_simulirani_potez(od_p, do_p, sta_jede)
                
                if potez_je_lanac:
                    evaluacija = self.minimax(trenutna_tabla, dubina - 1, alpha, beta, "PLAVA", trenutna_tabla.polozaji[do_p])
                else:
                    evaluacija = self.minimax(trenutna_tabla, dubina - 1, alpha, beta, "CRVENA", None)
                
                trenutna_tabla.polozaji = stari_okvir.polozaji
                
                min_eval = min(min_eval, evaluacija)
                beta = min(beta, min_eval)
                if beta <= alpha: # Alpha-Beta odsecanje
                    break
            
            self.upisi_u_transpozicionu_tabelu(trenutni_hash, dubina, min_eval)
            return min_eval

    def izracunaj_najbolji_potez(self, trenutna_tabla):
        """ Pokretač AI-ja koji koristi tehniku Iterativnog Produbljivanja """
        self.vreme_pocetka = time.time()
        

        svi_potezi = self.dobij_sve_moguce_poteze(trenutna_tabla, "CRVENA")
        #vraca niz poteza:(fig tren indeks, novi indeks, sta jede)

        if not svi_potezi:
            return None
            
        #ako ne stignemo izracunati sta je najbolje odigraj prvo sto mozes
        najbolji_potez = svi_potezi[0]
        
        # Iterative Deepening petlja - kopa progresivno sve dublje kroz nivoe
        for trenutna_dubina in range(1, 64):
            # Ako preostane manje od 0.4 sekunde za ceo sledeći nivo, prekidamo kopanje
            if time.time() - self.vreme_pocetka >= self.vremenski_limit - 0.4:
                break
                
            najbolji_skor = float('-inf')
            trenutni_izbor = najbolji_potez
            
            for od_p, do_p, sta_jede in svi_potezi:
                stari_okvir = GameState(trenutna_tabla.polozaji, "CRVENA", trenutna_tabla.lanac)
                potez_je_lanac = trenutna_tabla.izvrsi_simulirani_potez(od_p, do_p, sta_jede)
                
                if potez_je_lanac:
                    skor = self.minimax(trenutna_tabla, trenutna_dubina - 1, float('-inf'), float('inf'), "CRVENA", trenutna_tabla.polozaji[do_p])
                else:
                    skor = self.minimax(trenutna_tabla, trenutna_dubina - 1, float('-inf'), float('inf'), "PLAVA", None)
                    
                trenutna_tabla.polozaji = stari_okvir.polozaji
                
                if skor > najbolji_skor:
                    najbolji_skor = skor
                    trenutni_izbor = (od_p, do_p, sta_jede)
            
            # Ako nismo prešli limit u toku rada na ovoj dubini, potvrđujemo potez
            if time.time() - self.vreme_pocetka < self.vremenski_limit - 0.1:
                najbolji_potez = trenutni_izbor
                print(f"Završena dubina {trenutna_dubina}. Izabrani potez: {najbolji_potez}")
                
        return najbolji_potez