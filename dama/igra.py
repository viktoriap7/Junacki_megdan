import pygame
from dama.const import *
from dama.tabla import Tabla
class Igra:
    def __init__(self, proz):
        self.tren=None
        self.tabla=Tabla()
        self.na_redu=PLAVA
        self.pokreti={}
        self.proz=proz
    def update(self):
        self.tabla.nacrtaj(self.proz)
        pygame.display.update()