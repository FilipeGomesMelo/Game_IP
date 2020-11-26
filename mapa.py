import pygame as pg

# initialize Pygame
pg.init()

##################################################################################
#   Classe de Mapa provisório                                                    #
#   Essa classe assume que você está trabalhando com uma tela jogável de 672x672 #
##################################################################################
class mapa(object):
    def __init__(self, x, y, window):
        # cordenadas do mapa
        self.x = x
        self.y = y

        # tela em que o mapa vai ser colocado
        self.win = window

        # matriz 21x21 de um exemplo de mapa
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 1],
                    [1, 3, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 1],
                    [1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2],
                    [2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2],
                    [2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 1],
                    [1, 3, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 1],
                    [1, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
        # dicionário com as informações de cada tile diferente (imagem e tipo, vamos usar o tipo para calcualr colisão)
        self.tiles = {0: {'sprite': pg.transform.scale(pg.image.load('images/grass.png'), (32,32)), 'type': 'chao'},
                      1: {'sprite': pg.transform.scale(pg.image.load('images/tree.png'), (32,32)), 'type': 'parede'},
                      2: {'sprite': pg.transform.scale(pg.image.load('images/grass2.png'), (32,32)), 'type': 'spawn'},
                      3: {'sprite': pg.transform.scale(pg.image.load('images/tree2.png'), (32,32)), 'type': 'parede'},
                      4: {'sprite': pg.transform.scale(pg.image.load('images/grass3.png'), (32,32)), 'type': 'chao'}}
    
    # Desenha o mapa
    def draw(self):
        # Caminha por todos os números da matriz e desenha a imagem correspondente nas cordenadas correspondentes
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                self.win.blit(self.tiles[self.map[i][j]]['sprite'], (self.x+32*i, self.y+32*j))


