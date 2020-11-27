import pygame as pg
import math

# initialize Pygame
pg.init()

######################################################################################################
# classe responsavel pelos prejeteis do jogo, no momento somente o jogador consegue criar projeteis  #
######################################################################################################
class projectile(object):
    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT, direction):
        # define se a bala existe ou não
        self.existe = True

        # posição x e y da bala
        self.x = x
        self.y = y

        # lagura e altura da bala
        self.width = width
        self.height = height

        # tela em que a bala sera desenhada
        self.win = window
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        # vetor velocidade da bala
        self.vel = 0.5

        # sprite da bala
        self.img = pg.transform.scale(pg.image.load('images/bullet2.png'), (self.width,self.height))

        # direção é a chave para os sen e cos dessa bala
        self.direction = direction
        # angles é um dicionario com os senos e cosenos de cada angulo de 0 a 365 de 5 em 5
        self.angles = {}
    def check_enemy(self, enemies):
        corners = [[self.x, self.y], [self.x+self.width, self.y], [self.x, self.y+self.height], [self.x+self.width, self.y+self.height]]
        for enemy in enemies:
            for corner in corners:
                if enemy.x+1 < corner[0] < enemy.x + enemy.width and enemy.y < corner[1] < enemy.y + enemy.height:
                    self.existe = False
                    return enemy
        return -1

    def update(self, dt, mapa):
        # para permitir criar balas em novos angulos que não fazem parte do dicionário
 
        angle = self.direction*math.pi/180
        # calcula a velocidade x e y com base nos senos e cosenos (eixo y é invertido no pygame, multiplicamos por -1)
        speedX = self.vel*round(math.cos(angle),3)*dt
        speedY = -self.vel*round(math.sin(angle),3)*dt


        # calcula a nova posição da bala   
        self.x += speedX
        self.y += speedY


        if not(0 < self.x < self.WINDOW_WIDTH and 0 < self.y < self.WINDOW_HEIGHT) or not(0 < self.x + self.width < self.WINDOW_WIDTH and 0 < self.y < self.WINDOW_HEIGHT):
            self.existe = False
        if self.existe:
            if mapa.tiles[mapa.map[int(self.y//32)%21][int(self.x//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x)//32)%21]]['type'] == 'parede':
                self.existe = False

    # desenha essa bala
    def draw(self):
        self.win.blit(self.img, (self.x, self.y))
