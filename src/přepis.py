import sys
import random
import pygame
pygame.init()

rozliseni_okna = (1280, 960)
slova=("slovo a další a ještě jedno", "nic","něco jsem napsal")
vybrane=random.randint(0,len(slova)-1)
okno = pygame.display.set_mode(rozliseni_okna)
napsano=""
font=pygame.font.Font(None, 128)
text=font.render(slova[vybrane], True, (0, 0, 0))
while True:
    okno.fill((255,255,255)) 
    stisknute_klavesy = pygame.key.get_pressed()
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if udalost.type==pygame.KEYUP:
            if stisknute_klavesy[pygame.K_BACKSPACE]:
                napsano=napsano[:-1]
            else :
                napsano=napsano+str(udalost.unicode)

    text2=font.render(napsano, True, (0, 0, 0))
    okno.blit(text,(100,200))
    okno.blit(text2,(100,300))
    if napsano==slova[vybrane]:
        print("správně")
    pygame.display.update()

