import pygame as pg

# initialize Pygame
pg.init()

class item(object):
    def __init__(self, x, y, window, rand, t):
        self.t = t
        self.x = x
        self.y = y
        self.win = window

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
        elif 60 <= rand < 65:
            self.type = 'clock'
            self.width = 32
            self.height = 32

        self.img = {'coin': pg.transform.scale(pg.image.load('images/coin.png'), (18,18)),
                    'S_coin': pg.transform.scale(pg.image.load('images/coin_special.png'), (18,18)),
                    'boots': pg.transform.scale(pg.image.load('images/boots.png'), (26,26)),
                    'coffee': pg.transform.scale(pg.image.load('images/coffee.png'), (24,24)),
                    'multi_shot': pg.transform.scale(pg.image.load('images/multi_shot.png'), (32,32)),
                    'fast_shot': pg.transform.scale(pg.image.load('images/fast_shot.png'), (32,32)),
                    'clock': pg.transform.scale(pg.image.load('images/clock.png'), (32,32))}
        self.existes = True
        self.duration = 5000
    
    def player_colision(self, player):
        corners = [[self.x, self.y], [self.x+self.width, self.y], [self.x, self.y+self.height], [self.x+self.width, self.y+self.height]]

        for corner in corners:
            if player.x <= corner[0] <= player.x+player.width and player.y <= corner[1] <= player.y+player.height:
                self.existes = False
                return self.type
        return -1
            


    def update(self, t):
        if t - self.t >= self.duration:
            self.existes = False

    def draw(self):
        self.win.blit(self.img[self.type], (self.x, self.y))