import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.igra import Igra
PROZOR=pygame.display.set_mode((SIR_PROZORA,VIS_PROZORA))
pygame.display.set_caption('Junački megdan')

def main():
    run=True
    igra=Igra(PROZOR) 
    """ nisi dodala sat!!! """

    igra.tabla.nacrtaj_kvadrate(PROZOR)
    igra.tabla.napravi_tablu(PROZOR)
    #igra.tabla.test_tabla(PROZOR)
    """ 
    fig=tabla.vrati_fig(1)
    tabla.pomjeri(fig, 15) """
    pygame.display.update()
    while run:
        
        for dogadjaj in pygame.event.get():
            if dogadjaj.type==pygame.QUIT:
                run= False

            if dogadjaj.type==pygame.MOUSEBUTTONDOWN:
                poz=pygame.mouse.get_pos()
                igra.odabir_misem(poz)
                print("main")
        """         fig=tabla.vrati_fig(indeks)
                tabla.pomjeri(fig,16)
        tabla.nacrtaj(PROZOR) """
        pygame.display.update()  
    pygame.quit()
main()

