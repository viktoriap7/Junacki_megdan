import pygame
from dama.const import *
from dama.tabla import Tabla
from dama.igra import Igra
PROZOR=pygame.display.set_mode((SIR_PROZORA,VIS_PROZORA))
pygame.display.set_caption('Junački megdan')
def dobij_indeks_od_misa(poz):
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

def main():
    run=True
    igra=Igra(PROZOR) 
    """ nisi dodala sat!!! """

    igra.tabla.nacrtaj_kvadrate(PROZOR)
    igra.tabla.napravi_tablu(PROZOR)
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
                indeks=dobij_indeks_od_misa(poz)
        """         fig=tabla.vrati_fig(indeks)
                tabla.pomjeri(fig,16)
        tabla.nacrtaj(PROZOR) """
        pygame.display.update()  
    pygame.quit()
main()

