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

    def update(self, x, y, dt):
        # if self.x < x:
        #     self.x += self.vel * dt
        # else:
        #     self.x -= self.vel * dt

        dx = x - self.x
        dy = y - self.y

        rads = atan2(dy, dx)
        rads %= 2 * pi

        speedx = self.vel * round(math.cos(rads), 3) * dt
        speedy = self.vel * round(math.sin(rads), 3) * dt

        self.x += speedx
        self.y += speedy

    # def baleado(self):