import pygame, sys                                       
from pygame.locals import *
from random import randint


pygame.init()
tela = pygame.display.set_mode((928,640),0,32)
pygame.display.set_caption('teste')

fim = False
pos_M = 0
posI_M = 0
MenuConf = 0
MenuConf2 = 0
P1_M = (363, 251)
P2_M = (341, 328)
P3_M = (346, 403)
P4_M = (366, 479)
P_Atual_M = (363, 251)
MenuFundo = pygame.image.load('Menu inicial/JOGO - Menu Inicial.png')
CreditosFundo = pygame.image.load('Menu inicial/Tela de Créditos.png')
ControlesFundo = pygame.image.load('Menu inicial/Controles.png')
Select1_M = pygame.image.load('Menu inicial/Selecionar - Iniciar - Menu Inicial.png')
Select2_M = pygame.image.load('Menu inicial/Selecionar - Controles - Menu Inicial.png')
Select3_M = pygame.image.load('Menu inicial/Selecionar - Créditos - Menu Inicial.png')
Select4_M = pygame.image.load('Menu inicial/Selecionar - Sair - Menu Inicial.png')
musica_menu = pygame.mixer.music.load('Sonoplastia/Músicas/Rápido Vovô - Música Menu Inicial.mp3')
pygame.mixer.music.play(-1)
troca = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - mudar opção.wav')
troca.set_volume(0.55)
selecionar = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - selecionar opção.wav')
selecionar.set_volume(0.55)
SoundConf = 0
SoundConf2 = 0

while not fim:
    Teclas = pygame.key.get_pressed()
    if MenuConf2 == 0:
        tela.blit(MenuFundo, (0,0))
        if Teclas[K_UP] or Teclas[K_w]:
            if pos_M == 0 and SoundConf == 0:
                posI_M = 3
                troca.play()
                SoundConf = 3
            elif pos_M == 1 and SoundConf == 1:
                posI_M = 0
                troca.play()
                SoundConf = 0
            elif pos_M == 2 and SoundConf == 2:
                posI_M = 1
                troca.play()
                SoundConf = 1
            elif pos_M == 3 and SoundConf == 3:
                posI_M = 2
                troca.play()
                SoundConf = 2
                
        if Teclas[K_DOWN] or Teclas[K_s]:
            if pos_M == 0 and SoundConf == 0:
                posI_M = 1
                troca.play()
                SoundConf = 1
            elif pos_M == 1 and SoundConf == 1:
                posI_M = 2
                troca.play()
                SoundConf = 2
            elif pos_M == 2 and SoundConf == 2:
                posI_M = 3
                troca.play()
                SoundConf = 3
            elif pos_M == 3 and SoundConf == 3:
                posI_M = 0
                troca.play()
                SoundConf = 0
                
        if Teclas[K_RETURN]:
            if pos_M == 0:
                if MenuConf == 0 and SoundConf2 == 0:
                    selecionar.play()
                    #AÇÃO DO BOTÃO INICIAR, COLOCAR AQUI PRA COMEÇAR O JOGO
            if pos_M == 1:
                if MenuConf == 0 and SoundConf2 == 0:
                    selecionar.play()
                    MenuConf2 = 1
            if pos_M == 2:
                if MenuConf == 0 and SoundConf2 == 0:
                    selecionar.play()
                    MenuConf2 = 2
            if pos_M == 3:
                if MenuConf == 0 and SoundConf2 == 0:
                    selecionar.play()
                    fim = True

        SoundConf2 = 0
        if MenuConf2 == 0 and not Teclas[K_RETURN]:
            MenuConf = 0
                    
        if posI_M == 0 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_M = 0
        elif posI_M == 1 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_M = 1
        elif posI_M == 2 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_M = 2
        elif posI_M == 3 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_M = 3
            
        if posI_M == 0:
            P_Atual_M = P1_M
            tela.blit(Select1_M, (P_Atual_M))
        elif posI_M == 1:
            P_Atual_M = P2_M
            tela.blit(Select2_M, (P_Atual_M))
        elif posI_M == 2:
            P_Atual_M = P3_M
            tela.blit(Select3_M, (P_Atual_M))
        elif posI_M == 3:
            P_Atual_M = P4_M
            tela.blit(Select4_M, (P_Atual_M))
    elif MenuConf2 == 1:
        tela.blit(ControlesFundo, (0,0))
        SoundConf2 = 2
        if MenuConf2 == 1 and not Teclas[K_RETURN]:
            MenuConf = 1
            
        if Teclas[K_RETURN] and SoundConf2 == 2:
            if MenuConf == 1:
                selecionar.play()
                MenuConf2 = 0
    elif MenuConf2 == 2:
        tela.blit(CreditosFundo, (0,0))
        SoundConf2 = 3
        if MenuConf2 == 2 and not Teclas[K_RETURN]:
            MenuConf = 2
            
        if Teclas[K_RETURN] and SoundConf2 == 3:
            if MenuConf == 2:
                selecionar.play()
                MenuConf2 = 0

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
