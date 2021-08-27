import pygame as pg

# initialize Pygame
pg.init()

#####################
#  Classe de itens  #
#####################
class item(object):
    def __init__(self, x, y, window, rand, t):
        # quantidade de ticks no momento em que o item foi criado
        self.t = t

        # seleciona o item com um número aleatório 
        if 0 <= rand < 20:
            self.type = 'coin'
            self.width = 18
            self.height = 18
        elif 20 <= rand < 30:
            self.type = 'S_coin' 
            self.width = 18
            self.height = 18
        elif 30 <= rand < 40:
            self.type = 'boots'
            self.width = 26
            self.height = 26
        elif 40 <= rand < 50:
            self.type = 'coffee'
            self.width = 24
            self.height = 24
        elif 50 <= rand < 55:
            self.type = 'multi_shot'
            self.width = 32
            self.height = 32
        elif 55 <= rand < 60:
            self.type = 'fast_shot'
            self.width = 32
            self.height = 32
        elif 60 <= rand < 62:
            self.type = 'clock'
            self.width = 32
            self.height = 32

        # coordenadas do item
        self.x = x+16-self.width//2
        self.y = y+16-self.height//2

        # janela do item
        self.win = window

        # imformações dos itens
        self.img = {'coin': pg.transform.scale(pg.image.load('images/coin.png'), (18,18)),
                    'S_coin': pg.transform.scale(pg.image.load('images/coin_special.png'), (18,18)),
                    'boots': pg.transform.scale(pg.image.load('images/boots.png'), (26,26)),
                    'coffee': pg.transform.scale(pg.image.load('images/coffee2.png'), (24,24)),
                    'multi_shot': pg.transform.scale(pg.image.load('images/multi_shot2.png'), (32,32)),
                    'fast_shot': pg.transform.scale(pg.image.load('images/fast_shot2.png'), (32,32)),
                    'clock': pg.transform.scale(pg.image.load('images/clock2.png'), (32,32))}

        # determina se o item existe ou não            
        self.existes = True

        # tempo que o item vai existir antes de desaparecer
        self.duration = 5000
    
    # detecta colisão com o jogador
    def player_colision(self, player):
        # os quatro cantos da hitbox do item
        corners = [[self.x, self.y],
                   [self.x+self.width, self.y],
                   [self.x, self.y+self.height],
                   [self.x+self.width, self.y+self.height]]

        # checa se qualquer um dos quatro cantos está dentro do jogador
        for corner in corners:
            if player.x <= corner[0] <= player.x+player.width\
                and player.y <= corner[1] <= player.y+player.height:
                # destroi o item
                self.existes = False
                # e retorna o tipo de item que foi coletado
                return self.type
        return -1
            
    def update(self, t):
        # se o item existe a mais tempo do que deveria, destroi o item
        if t - self.t >= self.duration:
            self.existes = False

    def draw(self):
        # desenha o item
        self.win.blit(self.img[self.type], (self.x, self.y))