import pygame
from math import atan2, degrees, pi
import math

pygame.init()


class inimigo(object):

    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT):
        # posição x e y do jogador no mapa
        self.x = x
        self.y = y

        # largura e altura do jogador
        self.width = width
        self.height = height

        # janela em que o jogador vai ser desenhado e suas dimenções
        self.win = window
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        self.img = pygame.transform.scale(pygame.image.load('images/inimigo.png'), (self.width, self.height))

        self.vel = 0.10

    def draw(self):
        self.win.blit(self.img, (self.x, self.y))

    def maior_movimento_valido(self, dt, mapa, speedX, speedY):
        # a representa a diferença entre o tamanho real do sprite do jogador e da "hitbox" com o mapa
        # isso serve para cirar uma janela de px maior para passar por espaços pequenos de um tile
        a = 2

        # corners salva os extremos da "hitbox"
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # move o jogador somente se a posição final for em um bloco tipo 'chão'
        # basicamente, se eu for me mover para uma posição e essa posição não for válida, eu tento dnv com um px a menos
        # até encontrar uma posição em que eu possa me mover
        if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((corners[0][1]+speedX*dt)//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((corners[1][1]+speedX*dt)//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((corners[2][1]+speedX*dt)//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((corners[3][1]+speedX*dt)//32)%21]]['type'] != 'parede':
            self.x += speedX*dt
        else:
            # se a soma da posição velocidade for um tile que o jogador não deveria conseguir entrar, então
            # esses loops vão procurar o maior movimeno possível na direção dada pela velocidade
            if speedX < 0:
                x = self.x + speedX*dt
                while(x < self.x):
                    if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((x+a)//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((x+a)//32)%21]]['type'] != 'parede':
                        self.x = x
                        break
                    x+=1
            if speedX > 0:
                x = self.x + speedX*dt
                while(self.x < x):
                    if mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] != 'parede':
                        self.x = x
                        break
                    x-=1
        
        # atualiza corners agora que movemos o personagem no eixo x
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # mesma coisa que foi feita com o eixo x
        if mapa.tiles[mapa.map[int((corners[0][0]+speedY*dt)//32)%21][int((corners[0][1])//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[1][0]+speedY*dt)//32)%21][int((corners[1][1])//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[2][0]+speedY*dt)//32)%21][int((corners[2][1])//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((corners[3][0]+speedY*dt)//32)%21][int((corners[3][1])//32)%21]]['type'] != 'parede':
            self.y += speedY*dt
        else:
            # Mesma coisa que foi feita com a velocidade x
            if speedY < 0:
                y = self.y + speedY*dt
                while(y < self.y):
                    if mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[0][1])//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[1][1])//32)%21]]['type'] != 'parede':
                        self.y = y
                        break
                    y += 1
            if speedY > 0:
                y = self.y + speedY*dt
                while(y > self.y):
                    if mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[2][1])//32)%21]]['type'] != 'parede' and mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[3][1])//32)%21]]['type'] != 'parede':
                        self.y = y
                        break
                    y -= 1

    def update(self, x, y, dt, mapa):
        if x != -1 and y != -1:
            dx = x - self.x
            dy = y - self.y

            rads = atan2(dy, dx)
            rads %= 2 * pi
            
            speedX = self.vel * round(math.cos(rads), 3)
            speedY = self.vel * round(math.sin(rads), 3)
        else:
            speedX = 0
            speedY = 0

        self.maior_movimento_valido(dt, mapa, speedX, speedY)
