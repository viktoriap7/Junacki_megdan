import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.igra import Igra
from protivnik.zhash import Zobrist_hash
from protivnik.rac import Racun
PROZOR=pygame.display.set_mode((SIR_PROZORA,VIS_PROZORA))
pygame.display.set_caption('Junački megdan')

def main():
    run=True
    igra=Igra(PROZOR) 
    """ nisi dodala sat!!! """
    rac=Racun(igra)
    igra.tabla.nacrtaj_kvadrate(PROZOR)
    igra.tabla.napravi_tablu(PROZOR)
    clock = pygame.time.Clock()
    # igra.tabla.test_tabla(PROZOR)
    """ 
    fig=tabla.vrati_fig(1)
    tabla.pomjeri(fig, 15) """
    pygame.display.update()
    traje=None
    ceka_kraj = True
    while run:
        clock.tick(300)
        if igra.na_redu==CRVENA:
            rac.igraj()
            pygame.display.update()
            

        for dogadjaj in pygame.event.get():
            if dogadjaj.type==pygame.QUIT:
                run= False
                ceka_kraj=False

            if dogadjaj.type==pygame.MOUSEBUTTONDOWN and igra.na_redu==PLAVA:
                poz=pygame.mouse.get_pos()
                igra.odabir_misem(poz)
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
    
    # 4. Crta se unutrašnjost (SIVA pozadina)
    pygame.draw.rect(PROZOR,SIVA,popup_pravougaonik)
    
    # 5. Crta se ivica (CRNA boja, debljina ivice 4 piksela)
    pygame.draw.rect(PROZOR,CRNA,popup_pravougaonik,4)
    
    # 6. Renderujemo tekst koristeći tvoj FONT i BIJELA slova
    tekst_povrsina=FONT.render(text,True,BIJELA)
    
    # 7. Računamo poziciju teksta tako da bude tačno u centru našeg popup-a
    tekst_POPUP_RAZMAK_SIR=POPUP_RAZMAK_SIR+(POPUP_SIR-tekst_povrsina.get_width())//2
    tekst_POPUP_RAZMAK_VIS=POPUP_RAZMAK_VIS+(POPUP_VIS/2)-15  # Pomjereno malo gore da ne udara u slike
    PROZOR.blit(tekst_povrsina,(tekst_POPUP_RAZMAK_SIR,tekst_POPUP_RAZMAK_VIS))
    pygame.display.update()
    
    while ceka_kraj:
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                ceka_kraj = False
    pygame.quit()
main()

