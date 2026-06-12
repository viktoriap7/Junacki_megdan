import pygame
from copy import deepcopy
from dama.const import *
from dama.tabla import Tabla
from dama.igra import Igra
from protivnik.zhash import Zobrist_hash
from protivnik.rac import Racun
from dama.strukture import Stek,Stablo,Cvor
PROZOR=pygame.display.set_mode((SIR_PROZORA,VIS_PROZORA))
pygame.display.set_caption('Junački megdan')

def main():
    run=True
    igra=Igra(PROZOR) 
    """ nisi dodala sat!!! """
    rac=Racun(igra)
    potezi_plavog=Stek()
    igra.tabla.nacrtaj_kvadrate(PROZOR)
    igra.tabla.napravi_tablu(PROZOR)
    clock = pygame.time.Clock()
    cvor=Cvor(deepcopy(igra.tabla))
    stablo=Stablo(cvor)
    stablo.tren_cvor=cvor
    potez=deepcopy(igra)
    potezi_plavog.push(potez)
    # igra.tabla.test_tabla(PROZOR)
    """ 
    fig=tabla.vrati_fig(1)
    tabla.pomjeri(fig, 15) """
    pygame.display.update()
    traje=None
    prikaz_igre = True
    while run:
        clock.tick(300)
        if igra.na_redu==CRVENA:
            rac.igraj()
            pygame.display.update()
    
            potez=deepcopy(igra)
            potezi_plavog.push(potez)
            cvor=Cvor(deepcopy(igra.tabla))
            stablo.tren_cvor.dodaj_dijete(cvor)
            stablo.tren_cvor=cvor

            

        for dogadjaj in pygame.event.get():
            if dogadjaj.type==pygame.QUIT:
                run= False
            if dogadjaj.type==pygame.MOUSEBUTTONDOWN and igra.na_redu==PLAVA:

                poz=pygame.mouse.get_pos()
                x,y=poz
                if 10<x<10+ATRIBUTI_DUGME_SIR and ATRIBUTI_STIT_VIS<y<ATRIBUTI_STIT_VIS+ATRIBUTI_VIS:
                    if stablo.tren_cvor.roditelj!=None:
                        stablo.tren_cvor=stablo.tren_cvor.roditelj
                    print("UNDO")
                    igra=potezi_plavog.pop()
                    if igra!=-1:
                        print("obicno")
                        igra.tabla.nacrtaj(PROZOR)
                        pygame.display.update()
                        rac.igra=igra
                 
                    else:
                        print("minus 1")
                        igra=Igra(PROZOR)
                        
                        igra.tabla.napravi_tablu(PROZOR)
                        igra.tabla.nacrtaj(PROZOR)
                        igra.tabla.prikazi_tablu()
                        rac.igra=igra
                        potez=deepcopy(igra)
                        potezi_plavog.push(potez)
                    
                else:
                    rez=igra.odabir_misem(poz)
                    if rez:
                        cvor=Cvor(deepcopy(igra.tabla))
                        stablo.tren_cvor.dodaj_dijete(cvor)
                        stablo.tren_cvor=cvor
                print("main")
        traje=rac.ispitaj_trajanje()
        if traje:
            break
        pygame.display.update()
    if traje==CRNA:
        text="REMI"
    elif traje==CRVENA:
        text="POBJEDNIK: CRVENI IGRAC"
    else:
        text="POBJEDNIK: PLAVI IGRAC"
    popup_pravougaonik=pygame.Rect(POPUP_RAZMAK_SIR,POPUP_RAZMAK_VIS,POPUP_SIR,POPUP_VIS)
    pygame.draw.rect(PROZOR,SIVA,popup_pravougaonik)
    pygame.draw.rect(PROZOR,CRNA,popup_pravougaonik,4)
    
    tekst_povrsina=FONT.render(text,True,BIJELA)
    
    tekst_POPUP_RAZMAK_SIR=POPUP_RAZMAK_SIR+(POPUP_SIR-tekst_povrsina.get_width())//2
    tekst_POPUP_RAZMAK_VIS=POPUP_RAZMAK_VIS+(POPUP_VIS/2)-15  # Pomjereno malo gore da ne udara u slike
    PROZOR.blit(tekst_povrsina,(tekst_POPUP_RAZMAK_SIR,tekst_POPUP_RAZMAK_VIS))
    pygame.display.update()
    
    while prikaz_igre:

        for dogadjaj in pygame.event.get():
            if dogadjaj.type==pygame.QUIT:
                prikaz_igre = False
            if dogadjaj.type==pygame.MOUSEBUTTONDOWN:
                stablo.preorder(stablo.korijen,PROZOR)
    pygame.quit()
main()

