import pygame
import os
VIS_PROZORA=800
SIR_PROZORA=1200
VIS_TABLE=600
BR_KOL,BR_RED=8,8
KVADRAT=VIS_TABLE//BR_KOL
FIGURA=KVADRAT//3
SLIKA=FIGURA*2+3
RAZMAK_SIR=(SIR_PROZORA-VIS_TABLE)//2
RAZMAK_VIS=(VIS_PROZORA-VIS_TABLE)//2

ATRIBUTI_SIR=RAZMAK_SIR+VIS_TABLE+10
ATRIBUTI_VIS=RAZMAK_VIS

POPUP_SIR=400
POPUP_VIS=200
POPUP_RAZMAK_SIR=(SIR_PROZORA-POPUP_SIR)//2
POPUP_RAZMAK_VIS=(VIS_PROZORA-POPUP_VIS)//2
LIJEVO_POPUP_X=POPUP_RAZMAK_SIR
LIJEVO_POPUP_Y=POPUP_RAZMAK_VIS
DESNO_POPUP_X=POPUP_RAZMAK_SIR+(POPUP_SIR//2)
DESNO_POPUP_Y=POPUP_RAZMAK_VIS  
DUGME_SIR_POPUP=POPUP_SIR//2
DUGME_VIS_POPUP=POPUP_VIS
pygame.font.init()
FONT=pygame.font.Font(None,30)
""" boje """
BIJELA=(250,250,250)
CRNA=(10,10,10)
PLAVA=(10,10,250)
CRVENA=(250,10,10)
SIVA=(100,100,100)
ZELENA=(144, 252, 3)
ZUTA=(248,231,28)
SMEDJA=(87,37,9)
""" slike """
#RAW SLIKE
MARKO_PLAVI_RAW = pygame.image.load("slike/marko_plavi.png")
MARKO_CRVENI_RAW = pygame.image.load("slike/marko_crveni.png")
SHIELD_PLAVA_RAW = pygame.image.load("slike/shield_plava.png")
SHIELD_CRVENA_RAW = pygame.image.load("slike/shield_crvena.png")
CRENEL_CROWN_PLAVA_RAW = pygame.image.load("slike/crenel_crown_plava.png")
CRENEL_CROWN_CRVENA_RAW = pygame.image.load("slike/crenel_crown_crvena.png")
MACE_HEAD_PLAVA_RAW = pygame.image.load("slike/mace_head_plava.png")
MACE_HEAD_CRVENA_RAW = pygame.image.load("slike/mace_head_crvena.png")
DONKEY_PLAVI_RAW = pygame.image.load("slike/donkey_plavi.png")
DONKEY_CRVENI_RAW = pygame.image.load("slike/donkey_crveni.png")

#KONAČNE SLIKE
MARKO_PLAVI = pygame.transform.scale(MARKO_PLAVI_RAW, (SLIKA, SLIKA))
MARKO_CRVENI = pygame.transform.scale(MARKO_CRVENI_RAW, (SLIKA, SLIKA))
STIT_PLAVA = pygame.transform.scale(SHIELD_PLAVA_RAW, (SLIKA, SLIKA))
STIT_CRVENA = pygame.transform.scale(SHIELD_CRVENA_RAW, (SLIKA, SLIKA))
KRALJ_PLAVA = pygame.transform.scale(CRENEL_CROWN_PLAVA_RAW, (SLIKA, SLIKA))
KRALJ_CRVENA = pygame.transform.scale(CRENEL_CROWN_CRVENA_RAW, (SLIKA, SLIKA))
TOPUZ_PLAVA = pygame.transform.scale(MACE_HEAD_PLAVA_RAW, (SLIKA, SLIKA))
TOPUZ_CRVENA = pygame.transform.scale(MACE_HEAD_CRVENA_RAW, (SLIKA, SLIKA))
KONJ_PLAVI = pygame.transform.scale(DONKEY_PLAVI_RAW, (SLIKA, SLIKA))
KONJ_CRVENI = pygame.transform.scale(DONKEY_CRVENI_RAW, (SLIKA, SLIKA))