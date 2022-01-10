import pygame
from pygame.locals import *
from random import randint
import time
from time import sleep
from sys import exit

pygame.init()


game_over = 0
tile_size = 32
#___________________________________CARREGANDO IMAGENS__________________________________

#Paredes
par_esq = pygame.image.load('bordas/vertical.jpg')
par_dir = pygame.image.load('bordas/vertical.jpg')
par_baixo = pygame.image.load('bordas/horizontal.jpg')
par_cima = pygame.image.load('bordas/horizontal.jpg')
par_meio = pygame.image.load('bordas/meio.jpg')
fundo_hud = pygame.image.load('mapas/fundo_hud.png')

#Objetos

Fv1 = pygame.image.load('frutas/verdes/abacaxi 1.png')
Fv2 = pygame.image.load('frutas/verdes/abacaxi 2.png')
Fv3 = pygame.image.load('frutas/verdes/abacaxi 3.png')
Fv4 = pygame.image.load('frutas/verdes/banana 1.png')
Fv5 = pygame.image.load('frutas/verdes/banana 2.png')
Fv6 = pygame.image.load('frutas/verdes/banana 3.png')
Fv7 = pygame.image.load('frutas/verdes/pera 1.png')
Fv8 = pygame.image.load('frutas/verdes/pera 2.png')
Fv9 = pygame.image.load('frutas/verdes/pera 3.png')


#Mapas
mapa1 = pygame.image.load('mapas/mapa1.png')
mapa2 = pygame.image.load('mapas/mapa2.png')
mapa3 = pygame.image.load('mapas/mapa3.png')

#_______________________________________________________________________________________

#___________________________________CRIANDO O PERSONAGEM________________________________        

class Player:
    #Construtor/inicializador do player
    def __init__(self, x, y):
        #Movimentar o player
        self.images_right = []
        self.images_left = []
        self.images_back = []
        self.images_front = []
        self.index = 0
        self.counter = 0
        #Carregando as imagens da direita
        for num in range(1,5):
            #---- DIREITA E ESQUERDA
            img_right = pygame.image.load(f'vovo/vovo_dir{num}.png')
            #Escalonando para que estejam no tamanho desejado
            img_right = pygame.transform.scale(img_right, (32,64))
            #Invertendo a imagem para ter o personagem andando para esquerda
            img_left = pygame.transform.flip(img_right, True, False)
            #Adicionando a imagem na Lista de Imagens da direita
            self.images_right.append(img_right)
            #Adicionando a imagem na Lista de Imagens da esquerda
            self.images_left.append(img_left)

            #---- FRENTE E COSTAS
            img_back = pygame.image.load(f'vovo/vovo_costas{num}.png')
            img_front = pygame.image.load(f'vovo/vovo_frente{num}.png')
            img_back = pygame.transform.scale(img_back, (32,64))
            img_front = pygame.transform.scale(img_front, (32,64))
            self.images_back.append(img_back)
            self.images_front.append(img_front)

            
        #self.image = self.images_back[self.index]
        self.image = self.images_front[self.index]
        #Criando o retangulo na imagem    
        #self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #Variáveis do colisor
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #Variável para definir a direção do player
        self.direction = 0
        self.direcao = 0
        
    #Movimentos do player
    def update(self, game_over):
        dx = 0
        dy = 0

        #Velocidade do player
        speed = 4

        #Velocidade da animação do player
        walk_cooldown = 4
        
        
        if game_over == 0:
            #Pega a tecla pressionada
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                dx -= speed
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += speed
                self.counter += 1
                self.direction = 1
            if key[pygame.K_w]:
                dy -= speed
                self.counter += 1
                self.direcao = 1
            if key[pygame.K_s]:
                dy += speed
                self.counter += 1
                self.direcao = -1
            #Caso nenhuma tecla esteja sendo pressionada
            if key[pygame.K_a] == False and key[pygame.K_d] == False and key[pygame.K_w] == False and key[pygame.K_s] == False :
                self.counter = 0
                self.index = 0            
                #Direção da imagem quando para de apertar as teclas
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direcao == 1:
                    self.image = self.images_back[self.index]
                if self.direcao == -1:
                    self.image = self.images_front[self.index]
                    
	        
            #Animação do player
            if self.counter > walk_cooldown:
                self.counter = 0    
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0         
                #Movimentar para esquerda ou direita
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

                #Movimentar para cima ou baixo
                elif self.direcao == 1:
                    self.image = self.images_back[self.index]
                elif self.direcao == -1:
                    self.image = self.images_front[self.index]

            self.direction = 0
            self.direcao = 0
	        
            #Checando a colisão
            for tile in world.tile_list:
            #Checando colisão no eixo X
                if tile[1].colliderect(self.rect.x + dx, self.rect.y + 16, self.width, self.height - 16):
                    dx = 0
                #Checando colisão no eixo Y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy + 16, self.width, self.height - 16):
                    dy = 0
	           
            #Update das coordenadas do player
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #Desenha o player na tela
        screen.blit(self.image, self.rect)

        return game_over
#_______________________________________________________________________________________

#______________________________________CRIANDO UM MUNDO_________________________________

class World():
    def __init__(self, data):
        self.tile_list = []
        self.space_list = []

        #Carregando Mapa1
        colisor_img = pygame.image.load('mapas/colisor.png')
        colisor1_img = pygame.image.load('mapas/colisor1.png')
        #Contador de linha
        row_count = 0
        for row in data:
            #Contador de coluna
            col_count = 0
            for tile in row:
                #Se o valor de (x,y) for igual a 1
                if tile == 1:
                    img = pygame.transform.scale(colisor_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                #Se o valor de (x,y) for igual a 2
                if tile == 2:
                    fruit = Frutas(col_count * tile_size, row_count * tile_size)
                    frutas_grupo.add(fruit)
                    self.space_list.append([col_count * tile_size, row_count * tile_size])
                    print(frutas_grupo)
                    print(lista_hud)
                    
                    #Colisor para interagir com a fruta
                    img = pygame.transform.scale(colisor_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #Se o valor de (x,y) for igual a 1
                if tile == 4:
                    img = pygame.transform.scale(colisor1_img, (tile_size, 12))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #Próxima coluna na linha x
                col_count += 1
            #Próxima linha
            row_count += 1
    #Mostrando na tela a lista de mundo
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
#________________________________________________________________________________________

#_______________________________________FRUTAS___________________________________________

lista_hud = []

c0 = 0
c1 = 0
c2 = 0
c3 = 0

class Frutas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global c0, c1, c2, c3
        self.lista1 = []
        img1 = 'frutas/morango1.png'
        img2 = 'frutas/laranja1.png'
        img3 = 'frutas/melancia1.png'
        img4 = 'frutas/maça1.png'
        self.lista1.append(img1)
        self.lista1.append(img2)
        self.lista1.append(img3)
        self.lista1.append(img4)
        j = randint(0,3)

        if j == 0:
        	if c0<3:
        		lista_hud.append(j)
        		c0 += 1
        if j == 1:
        	if c1<3:
        		lista_hud.append(j)
        		c1 += 1
        if j == 2:
        	if c2<3:
        		lista_hud.append(j)
        		c2 += 1
        if j == 3:
        	if c3<3:
        		lista_hud.append(j)
        		c3 += 1
        #print(lista_hud)
        self.image = pygame.transform.scale(pygame.image.load(self.lista1[j]), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x - 16
        self.rect.y = y - 16
#________________________________________________________________________________________

#_____________________________POSIÇÃO DAS COISAS NO MUNDO________________________________
#MAPA1
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1], 
[1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 2, 1, 1, 0, 1], 
[1, 1, 1, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 1, 1, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 1, 1, 1, 0, 0, 1],  
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
#MAPA2
world_data2 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 1], 
[1, 0, 1, 2, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], 
[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 4, 4, 0, 1], 
[1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1], 
[1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1], 
[1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 2, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],  
[1, 0, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
#MAPA3
world_data3 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 0, 0, 1, 1, 0, 0, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 0, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1], 
[1, 0, 0, 1, 0, 4, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 1, 2, 0, 1], 
[1, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
[1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  
[1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1], 
[1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
#_______________________________________________________________________________________

def Voltar():
      
    fim = False
    pos_M = 0
    posI_M = 0
    MenuConf = 0
    MenuConf2 = 0
    voltmenu = 0
    voltmenu2 = 0
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
            screen.blit(MenuFundo, (0,0))
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
                        Menu()
                     #AÇÃO DO BOTÃO INICIAR, COLOCAR AQUI PRA COMEÇAR O JOGO
                    # ESSE IF, TEM Q SER APERTADO UMA VEZ SÓ
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
                        exit()
                        

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
                screen.blit(Select1_M, (P_Atual_M))
            elif posI_M == 1:
                P_Atual_M = P2_M
                screen.blit(Select2_M, (P_Atual_M))
            elif posI_M == 2:
                P_Atual_M = P3_M
                screen.blit(Select3_M, (P_Atual_M))
            elif posI_M == 3:
                P_Atual_M = P4_M
                screen.blit(Select4_M, (P_Atual_M))
        elif MenuConf2 == 1:
            screen.blit(ControlesFundo, (0,0))
            SoundConf2 = 2
            if MenuConf2 == 1 and not Teclas[K_RETURN]:
                MenuConf = 1
                
            if Teclas[K_RETURN] and SoundConf2 == 2:
                if MenuConf == 1:
                    selecionar.play()
                    MenuConf2 = 0
        elif MenuConf2 == 2:
            screen.blit(CreditosFundo, (0,0))
            SoundConf2 = 3
            if MenuConf2 == 2 and not Teclas[K_RETURN]:
                MenuConf = 2
                
            if Teclas[K_RETURN] and SoundConf2 == 3:
                if MenuConf == 2:
                    selecionar.play()
                    MenuConf2 = 0

        Exit()
        pygame.display.update()
         
def Menu():
    global start,pause
    
    start = False
    pause = False
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
            screen.blit(MenuFundo, (0,0))
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
                        Fase1()
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
                        exit()
                        

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
                screen.blit(Select1_M, (P_Atual_M))
            elif posI_M == 1:
                P_Atual_M = P2_M
                screen.blit(Select2_M, (P_Atual_M))
            elif posI_M == 2:
                P_Atual_M = P3_M
                screen.blit(Select3_M, (P_Atual_M))
            elif posI_M == 3:
                P_Atual_M = P4_M
                screen.blit(Select4_M, (P_Atual_M))
        elif MenuConf2 == 1:
            screen.blit(ControlesFundo, (0,0))
            SoundConf2 = 2
            if MenuConf2 == 1 and not Teclas[K_RETURN]:
                MenuConf = 1
                
            if Teclas[K_RETURN] and SoundConf2 == 2:
                if MenuConf == 1:
                    selecionar.play()
                    MenuConf2 = 0
        elif MenuConf2 == 2:
            screen.blit(CreditosFundo, (0,0))
            SoundConf2 = 3
            if MenuConf2 == 2 and not Teclas[K_RETURN]:
                MenuConf = 2
                
            if Teclas[K_RETURN] and SoundConf2 == 3:
                if MenuConf == 2:
                    selecionar.play()
                    MenuConf2 = 0

        Exit()
        pygame.display.update()
        
        
def Fase1():
        global minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, play, game_over, fps, timer, ganhar, pontos
        
        
        musica_fase = pygame.mixer.music.load('Sonoplastia/Músicas/Rápido Vovô - Música Fases (rápida).mp3')
        pygame.mixer.music.play(-1)
        pontos = 0
        start = True
        while start:
            clock.tick(fps)
            
            screen.blit(par_esq, (0,0))
            screen.blit(par_dir, (scr_lar-32,0))
            screen.blit(par_cima, (32,0))
            screen.blit(par_baixo, (32,scr_alt-32))
            screen.blit(par_meio, (608,32))
            screen.blit(fundo_hud, (0,0))
            screen.blit(mapa1, (32,32))
            screen.blit(Fv4, (159,100))
            screen.blit(Fv1, (550,67))
            screen.blit(Fv7, (327,228))
            screen.blit(Fv8, (70,260))
            screen.blit(Fv2, (260,419))
            screen.blit(Fv5, (487,454))
            point = f'Pontos:{pontos}'
            ponto = fonte.render(point, True, (83,45,34))
            #------------------------------ CRONOMETRO --------------------------------
            #Contando os milissegundos
            time = f'{minuto}:{segundo}'
            cronometro = fonte.render(time, True, (83,45,34))
            milissegundo -= 5
            if milissegundo == 0 and segundo >=0:
                milissegundo = 100
                segundo -= 1
            if segundo > 60:
                minuto = 1  
            if segundo < 60:
                minuto = 0
            #Quando o tempo acabar, Gameover
            if segundo <= 0:
                segundo = 0
                minuto = 0
                Gameover()
            #Mostrando o cronometro na tela
            #screen.blit(ponto,(680,95))
            screen.blit(cronometro, (705,475))
            if pontos >= 8:
                Ganhar()
                if pygame.key.get_pressed()[K_RETURN]: 
                            Fase2() 
            #--------------------------------------------------------------------------
            Pegar1()
            if pygame.key.get_pressed()[K_p]:
                Pause1()

            frutas_grupo.draw(screen)
            game_over = player.update(game_over)
            
            #Sair do jogo    
            Exit()
            pygame.display.update()
                
def Fase2():
        global minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, play, game_over, fps, timer, ganhar, pontos, c0, c1, c2, c3, lista_hud
        c0 = 0
        c1 = 0
        c2 = 0
        c3 = 0
        lista_hud.clear()        
        player = Player(64,32)
        frutas_grupo = pygame.sprite.Group()
        world = World(world_data2)
        pontos = 0
        start = True
        while start:
            
            clock.tick(fps)
            
            screen.blit(par_esq, (0,0))
            screen.blit(par_dir, (scr_lar-32,0))
            screen.blit(par_cima, (32,0))
            screen.blit(par_baixo, (32,scr_alt-32))
            screen.blit(par_meio, (608,32))
            screen.blit(fundo_hud, (0,0))
            screen.blit(mapa2, (32,32))
            screen.blit(Fv1, (394,100))
            screen.blit(Fv7, (577,107))
            screen.blit(Fv4, (577,289))
            screen.blit(Fv8, (490,259))
            screen.blit(Fv5, (288,141))
            screen.blit(Fv2, (167,351))
            screen.blit(Fv6, (73,258))
            screen.blit(Fv3, (464,391))
            screen.blit(Fv9, (381,513))
            point = f'Pontos:{pontos}'
            ponto = fonte.render(point, True, (83,45,34))
            #------------------------------ CRONOMETRO --------------------------------
            #Contando os milissegundos
            time = f'{minuto}:{segundo}'
            cronometro = fonte.render(time, True, (83,45,34))
            milissegundo -= 5
            if milissegundo == 0 and segundo >=0:
                milissegundo = 100
                segundo -= 1
            if segundo > 60:
                minuto = 1  
            if segundo < 60:
                minuto = 0
            #Quando o tempo acabar, Gameover
            if segundo <= 0:
                segundo = 0
                minuto = 0
                Gameover2()
            #Mostrando o cronometro na tela
            #screen.blit(ponto,(680,95))
            screen.blit(cronometro, (705,475))
            if pontos >= 10:
                Ganhar()
                if pygame.key.get_pressed()[K_RETURN]: 
                    Fase3()   
            #--------------------------------------------------------------------------
            Pegar1()
            if pygame.key.get_pressed()[K_p]:
                Pause2()

            frutas_grupo.draw(screen)
            game_over = player.update(game_over)  
        
            #Sair do jogo        
            Exit()
            pygame.display.update()

def Fase3():
        global minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, play, game_over, fps, timer, ganhar, pontos, c0, c1, c2, c3, lista_hud
        c0 = 0
        c1 = 0
        c2 = 0
        c3 = 0
        lista_hud.clear()
        player = Player(204,30)
        frutas_grupo = pygame.sprite.Group()
        world = World(world_data3)
        pontos = 0
        start = True
        while start:
            
            clock.tick(fps)
            
            screen.blit(par_esq, (0,0))
            screen.blit(par_dir, (scr_lar-32,0))
            screen.blit(par_cima, (32,0))
            screen.blit(par_baixo, (32,scr_alt-32))
            screen.blit(par_meio, (608,32))
            screen.blit(fundo_hud, (0,0))
            screen.blit(mapa3, (32,32))
            screen.blit(Fv4, (119,74))
            screen.blit(Fv7, (155,557))
            screen.blit(Fv1, (546,176))
            screen.blit(Fv2, (99,257))
            screen.blit(Fv5, (336,236))
            screen.blit(Fv6, (153,355))
            screen.blit(Fv8, (282,395))
            screen.blit(Fv9, (399,426))
            screen.blit(Fv3, (247,500))
            point = f'Pontos:{pontos}'
            ponto = fonte.render(point, True, (83,45,34))
            #------------------------------ CRONOMETRO --------------------------------
            #Contando os milissegundos
            time = f'{minuto}:{segundo}'
            cronometro = fonte.render(time, True, (83,45,34))
            milissegundo -= 5
            if milissegundo == 0 and segundo >=0:
                milissegundo = 100
                segundo -= 1
            if segundo > 60:
                minuto = 1  
            if segundo < 60:
                minuto = 0
            #Quando o tempo acabar, Gameover
            if segundo <= 0:
                segundo = 0
                minuto = 0
                Gameover3()
            #Mostrando o cronometro na tela
            #screen.blit(ponto,(680,95))
            screen.blit(cronometro, (705,475))
            if pontos >= 18:
                Ganhar()
                if pygame.key.get_pressed()[K_RETURN]:
                    exit()
            #--------------------------------------------------------------------------
            Pegar1()
            if pygame.key.get_pressed()[K_p]:
                Pause3()
        
            frutas_grupo.draw(screen)
            game_over = player.update(game_over)  
                
            #Sair do jogo        
            Exit()
            pygame.display.update()

#_____________________________________PAUSE DO JOGO_____________________________________
def Pause1():

    pause = True
    pos_P = 0
    posI_P = 0
    PauseConf = 0
    PauseConf2 = 0
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
    while pause:
        
        screen.blit(MenuPause, (0,0))
        
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

        if Teclas[K_RETURN]:
            if pos_P == 0:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    #BOTÃO PARA RETOMAR O JOGO E CONTINUAR
            if pos_P == 1:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    Reiniciar()
                    #BOTÃO RECOMEÇAR PARA RECOMEÇAR O JOGO
            if pos_P == 2:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    Voltar()
                    #BOTÃO SAIR COLOCAR PRA IR PRO MENU
                
        if posI_P == 0 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 0
        elif posI_P == 1 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 1
        elif posI_P == 2 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 2
            
        if posI_P == 0:
            P_Atual_P = P1_P
            screen.blit(Select1_P, (P_Atual_P))
        elif posI_P == 1:
            P_Atual_P = P2_P
            screen.blit(Select2_P, (P_Atual_P))
        elif posI_P == 2:
            P_Atual_P = P3_P
            screen.blit(Select3_P, (P_Atual_P))
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pause = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()


def Pause2():
    
    pause = True
    pos_P = 0
    posI_P = 0
    PauseConf = 0
    PauseConf2 = 0
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
    while pause:
        
        screen.blit(MenuPause, (0,0))
        
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

        if Teclas[K_RETURN]:
            if pos_P == 0:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    #BOTÃO PARA RETOMAR O JOGO E CONTINUAR
            if pos_P == 1:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    Reiniciar2()
                    #BOTÃO RECOMEÇAR PARA RECOMEÇAR O JOGO
            if pos_P == 2:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    exit()
                    #BOTÃO SAIR COLOCAR PRA IR PRO MENU
                
        if posI_P == 0 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 0
        elif posI_P == 1 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 1
        elif posI_P == 2 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 2
            
        if posI_P == 0:
            P_Atual_P = P1_P
            screen.blit(Select1_P, (P_Atual_P))
        elif posI_P == 1:
            P_Atual_P = P2_P
            screen.blit(Select2_P, (P_Atual_P))
        elif posI_P == 2:
            P_Atual_P = P3_P
            screen.blit(Select3_P, (P_Atual_P))
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pause = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

def Pause3():
    
    pause = True
    pos_P = 0
    posI_P = 0
    PauseConf = 0
    PauseConf2 = 0
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
    while pause:
        
        screen.blit(MenuPause, (0,0))
        
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

        if Teclas[K_RETURN]:
            if pos_P == 0:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    #BOTÃO PARA RETOMAR O JOGO E CONTINUAR
            if pos_P == 1:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    pause = False
                    Reiniciar3()
                    #BOTÃO RECOMEÇAR PARA RECOMEÇAR O JOGO
            if pos_P == 2:
                if PauseConf == 0 and SoundConf2_P == 0:
                    selecionar.play()
                    exit()
                    #BOTÃO SAIR COLOCAR PRA IR PRO MENU
                
        if posI_P == 0 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 0
        elif posI_P == 1 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 1
        elif posI_P == 2 and not Teclas[K_UP] and not Teclas[K_DOWN] and not Teclas[K_w] and not Teclas[K_s]:
            pos_P = 2
            
        if posI_P == 0:
            P_Atual_P = P1_P
            screen.blit(Select1_P, (P_Atual_P))
        elif posI_P == 1:
            P_Atual_P = P2_P
            screen.blit(Select2_P, (P_Atual_P))
        elif posI_P == 2:
            P_Atual_P = P3_P
            screen.blit(Select3_P, (P_Atual_P))
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pause = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
#_______________________________________________________________________________________
def Reiniciar():
    global  timer, minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, pontos, c0, c1, c2, c3, lista_hud
        
    c0 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    
    musica_fase = pygame.mixer.music.load('Sonoplastia/Músicas/Rápido Vovô - Música Fases (rápida).mp3')
    pygame.mixer.music.play(-1)
    lista_hud.clear()
    timer = True
    pontos = int (0)
    minuto = int (0)
    segundo = int (15)
    milissegundo = int (100)
    perdeu = False
    player = Player(64,32)
    frutas_grupo = pygame.sprite.Group()
    world = World(world_data)
    pontos = 0
    
def Reiniciar2():
    global  timer, minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, pontos, c0, c1, c2, c3, lista_hud
        
    c0 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    
    musica_fase = pygame.mixer.music.load('Sonoplastia/Músicas/Rápido Vovô - Música Fases (rápida).mp3')
    pygame.mixer.music.play(-1)
    lista_hud.clear()
    timer = True
    pontos = int (0)
    minuto = int (0)
    segundo = int (15)
    milissegundo = int (100)
    perdeu = False
    player = Player(64,32)
    frutas_grupo = pygame.sprite.Group()
    world = World(world_data2)
    pontos = 0
    
def Reiniciar3():
    global  timer, minuto, segundo, milissegundo, player, frutas_grupo, world, perdeu, pontos, c0, c1, c2, c3, lista_hud

    c0 = 0
    c1 = 0
    c2 = 0
    c3 = 0

    musica_fase = pygame.mixer.music.load('Sonoplastia/Músicas/Rápido Vovô - Música Fases (rápida).mp3')
    pygame.mixer.music.play(-1)
    lista_hud.clear()
    timer = True
    pontos = int (0)
    minuto = int (0)
    segundo = int (15)
    milissegundo = int (100)
    perdeu = False
    player = Player(204,30)
    frutas_grupo = pygame.sprite.Group()
    world = World(world_data3)
    pontos = 0
       
def Gameover():
    global perdeu
    timer_over = pygame.mixer.music.load('Sonoplastia/Efeitos sonoros/Rápido Vovô - Game Over (online-audio-converter.com).mp3')
    pygame.mixer.music.play(0)
    perdeu = True
    while perdeu:
        
        gameover = pygame.image.load('Hud/Game Over.png')
        screen.blit(gameover, (0,0))
        time = f'{minuto}:{segundo}'
        cronometro = fonte.render(time, True, (83,45,34))
        screen.blit(cronometro, (705,475))
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    Reiniciar()               
        pygame.display.update()

def Gameover2():
    global perdeu
    timer_over = pygame.mixer.music.load('Sonoplastia/Efeitos sonoros/Rápido Vovô - Game Over (online-audio-converter.com).mp3')
    pygame.mixer.music.play(0)
    perdeu = True
    while perdeu:
        
        gameover = pygame.image.load('Hud/Game Over.png')
        screen.blit(gameover, (0,0))
        time = f'{minuto}:{segundo}'
        cronometro = fonte.render(time, True, (83,45,34))
        screen.blit(cronometro, (705,475))
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    Reiniciar2()               
        pygame.display.update()

def Gameover3():
    global perdeu
    timer_over = pygame.mixer.music.load('Sonoplastia/Efeitos sonoros/Rápido Vovô - Game Over (online-audio-converter.com).mp3')
    pygame.mixer.music.play(0)
    perdeu = True
    while perdeu:
        
        gameover = pygame.image.load('Hud/Game Over.png')
        screen.blit(gameover, (0,0))
        time = f'{minuto}:{segundo}'
        cronometro = fonte.render(time, True, (83,45,34))
        screen.blit(cronometro, (705,475))
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    Reiniciar3()               
        pygame.display.update()
                        
def Pegar1():
    global segundo, item, lista_hud, pontos, c0, c1, c2, c3
    pegou = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - chime pegar a fruta.wav')
    pegou.set_volume(0.55)    
    img_hud1 = pygame.image.load('hud/morangohud.png')
    img_hud2 = pygame.image.load('hud/laranjahud.png')
    img_hud3 = pygame.image.load('hud/melanciahud.png')
    img_hud4 = pygame.image.load('hud/maçahud.png')
    cont_morango = 0
    cont_laranja = 0
    cont_melancia = 0
    cont_maca = 0
    j = 0

    #Coordenadas da fruta HUD
    posx = 680
    posy = 110
    #Distancia entre frutas
    posplus = 60
    #Coordenadas da quantidade HUD
    phx = 770
    phy = 130
    #Disntancia entre quantidades
    phplus = 60
    #Contando as frutas
    while j<len(lista_hud):
    	if lista_hud[j] == 0:
    	    cont_morango += 1
    	if lista_hud[j] == 1:
    	    cont_laranja += 1
    	if lista_hud[j] == 2:
    	    cont_melancia += 1
    	if lista_hud[j] == 3:
    	    cont_maca += 1
    	j += 1
    #Inserindo as frutas na Lista do Vovô
    if cont_morango == 0:
    	screen.blit(img_hud2, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud3, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud4, (posx, posy))
    	#Inserindo a quantidade delas na lista
    	screen.blit(pygame.image.load(f'hud/hud{c1}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c2}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c3}.png'),(phx, phy))
    	phy += phplus

    elif cont_laranja == 0:
    	screen.blit(img_hud1, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud3, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud4, (posx, posy))
    	#Inserindo a quantidade delas na lista
    	screen.blit(pygame.image.load(f'hud/hud{c0}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c2}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c3}.png'),(phx, phy))
    	phy += phplus

    elif cont_melancia == 0:
    	screen.blit(img_hud1, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud2, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud4, (posx, posy))
    	#Inserindo a quantidade delas na lista
    	screen.blit(pygame.image.load(f'hud/hud{c0}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c1}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c3}.png'),(phx, phy))
    	phy += phplus

    elif cont_maca == 0:
    	screen.blit(img_hud1, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud2, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud3, (posx, posy))
    	#Inserindo a quantidade delas na lista
    	screen.blit(pygame.image.load(f'hud/hud{c0}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c1}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c2}.png'),(phx, phy))
    	phy += phplus

    else:
    	screen.blit(img_hud1, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud2, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud3, (posx, posy))
    	posy += posplus
    	screen.blit(img_hud4, (posx, posy))
    	#Inserindo a quantidade delas na lista
    	screen.blit(pygame.image.load(f'hud/hud{c0}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c1}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c2}.png'),(phx, phy))
    	phy += phplus
    	screen.blit(pygame.image.load(f'hud/hud{c3}.png'),(phx, phy))
    	phy += phplus

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if pygame.sprite.spritecollide(player, frutas_grupo, True):
                        f_inx = 0
                        f_iny = 0
                        f_finx = 0
                        f_finy = 0
                        jogadorx = player.rect.x
                        jogadory = player.rect.y+32
                        i = 0
                        j = 0
                        while i < len(world.space_list):
                        	f_inx = world.space_list[i][0]-32
                        	f_iny = world.space_list[i][1]-32
                        	f_finx = f_inx + 96
                        	f_finy = f_iny + 96

                        	if (f_inx<=jogadorx<=f_finx and f_iny<=jogadory<=f_finy):
                        		print(lista_hud[i])
                        		if c0 != 0:
	                        		if lista_hud[i] == 0:
	                        			c0 -= 1
	                        			print(c0)
                        		if c1 != 0:
	                        		if lista_hud[i] == 1:
	                        			c1 -= 1
	                        			print(c1)
                        		if c2 != 0:
	                        		if lista_hud[i] == 2:
	                        			c2 -= 1
	                        			print(c2)
                        		if c3 != 0:
	                        		if lista_hud[i] == 3:
	                        			c3 -= 1
	                        			print(c3)
                        	i += 1
                        pegou.play()
                        segundo += 500
                        pontos += 1
                    
def Exit():
    global run, fim, pause
                  
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
                run = False
                fim = False
                pause = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                    run = False
                    fim = False
                    pause = False
def Ganhar():
    global scr_alt,scr_lar
    
    boa = pygame.mixer.Sound('Sonoplastia/Efeitos sonoros/Rápido Vovô - chime ganhar a fase.wav')
    boa.set_volume(2)
    boa.play()
    ganhar = pygame.transform.scale(pygame.image.load('Hud/Ganhar fase.png'), (scr_lar, scr_alt))
    sair = True
    while sair:
        
        screen.blit(ganhar, (0,0))
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    sair = False
    
        pygame.display.update() 
                
        for event in pygame.event.get():
                if event.type == QUIT:
                    pause = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()        
                 
            
            

    
    
                
#___________________________________VARIÁVEIS GLOBAIS___________________________________



#Tempo da passagem de frames e contadores de tempo
perdeu = False
clock = pygame.time.Clock()
fps = 50 
timer = True
pontos = int (0)
minuto = int (0)
segundo = int (15)
milissegundo = int (10)
#Fonte do cronometro
fonte = pygame.font.SysFont('times new roman', 50, True,True)

#Altura e Largura da tela
scr_alt = 640
scr_lar = 928
#Display da tela
screen = pygame.display.set_mode((scr_lar, scr_alt))
pygame.display.set_caption ("Rápido Vovô!")

#Variável para criação do player na posição determinada entre ()
player = Player(64,32)

#Variável para criação do grupo Frutas
frutas_grupo = pygame.sprite.Group()

#Variável para a criação do mundo com a lista
world = World(world_data)

#Variável que diz quando o jogo está rodando e quando ele para
run = True
#_______________________________________START GAME______________________________________

while run:
    Exit()
    Menu()
        
           
    pygame.display.update()

pygame.quit()
