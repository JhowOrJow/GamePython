import pygame, sys                                       
from pygame.locals import *
from random import randint


pygame.init()
tela = pygame.display.set_mode((928,640),0,32)
pygame.display.set_caption('teste')

fim = False
pos_P = 0
posI_P = 0
P1_P = (209, 298)
P2_P = (196, 374)
P3_P = (228, 456)
P_Atual_P = (209, 298)
MenuPause = pygame.image.load('Menu pause/JOGO - Menu Pause.png')
Select1_P = pygame.image.load('Menu pause/Selecionar - Retomar - Menu de Pause.png')
Select2_P = pygame.image.load('Menu pause/Selecionar - Recomeçar - Menu de Pause.png')
Select3_P = pygame.image.load('Menu pause/Selecionar - Sair - Menu de Pause.png')
troca = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - mudar opção.wav')
troca.set_volume(0.55)
selecionar = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - selecionar opção.wav')
selecionar.set_volume(0.55)
SoundConf_P = 0
SoundConf2_P = 0


while not fim:
    tela.blit(MenuPause, (0,0))

    Teclas = pygame.key.get_pressed()
    if Teclas[K_UP] or Teclas[K_w]:
        if pos_P == 0 and SoundConf_P == 0:
            posI_P = 2
            troca.play()
            SoundConf_P = 2
        elif pos_P == 1 and SoundConf_P == 1:
            posI_P = 0
            troca.play()
            SoundConf_P = 0
        elif pos_P == 2 and SoundConf_P == 2:
            posI_P = 1
            troca.play()
            SoundConf_P = 1
    elif Teclas[K_DOWN] or Teclas[K_s]:
        if pos_P == 0 and SoundConf_P == 0:
            posI_P = 1
            troca.play()
            SoundConf_P = 1
        elif pos_P == 1 and SoundConf_P == 1:
            posI_P = 2
            troca.play()
            SoundConf_P = 2
        elif pos_P == 2 and SoundConf_P == 2:
            posI_P = 0
            troca.play()
            SoundConf_P = 0
            
    if posI_P == 0 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
        pos_P = 0
    elif posI_P == 1 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
        pos_P = 1
    elif posI_P == 2 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
        pos_P = 2
        
    if posI_P == 0:
        P_Atual_P = P1_P
        tela.blit(Select1_P, (P_Atual_P))
    elif posI_P == 1:
        P_Atual_P = P2_P
        tela.blit(Select2_P, (P_Atual_P))
    elif posI_P == 2:
        P_Atual_P = P3_P
        tela.blit(Select3_P, (P_Atual_P))
        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            fim = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.time.delay(12)

pygame.display.quit()
print("\n\nFim do programa.")
