import pygame as pg

# initialize Pygame
pg.init()

##################################################################################
#   Classe de Mapa provisório                                                    #
#   Essa classe assume que você está trabalhando com uma tela jogável de 672x672 #
##################################################################################
class mapa(object):
    def __init__(self, x, y, window, chave):
        # cordenadas do mapa
        self.x = x
        self.y = y

        # tela em que o mapa vai ser colocado
        self.win = window

        # dicionário dos mapas, cada casa representa um tile no mapa final
        self.mapas ={
                'mapa1': 
                    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 10, 10, 10, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 10, 10, 10, 1],
                    [1, 10, 4, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 10, 1],
                    [1, 10, 4, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 4, 10, 1],
                    [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1],
                    [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6, 1],
                    [1, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 7, 0, 3, 0, 0, 3, 0, 4, 1],
                    [1, 4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6, 0, 0, 4, 1],
                    [1, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 7, 0, 0, 0, 4, 1],
                    [2, 4, 0, 0, 1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 6, 0, 6, 0, 7, 4, 2],
                    [2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2],
                    [2, 4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 4, 2],
                    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 4, 1],
                    [1, 5, 8, 5, 8, 9, 8, 5, 9, 5, 8, 5, 9, 5, 8, 5, 8, 5, 9, 5, 1],
                    [1, 4, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 1],
                    [1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1],
                    [1, 6, 0, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 6, 1],
                    [1, 10, 4, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 3, 0, 0, 4, 10, 1],
                    [1, 10, 4, 4, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 10, 1],
                    [1, 10, 10, 10, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 10, 10, 10, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                'mapa2': 
                    [[26, 26, 26, 26, 26, 26, 26, 26, 26, 27, 27, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26],
                    [26, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 26],
                    [26, 30, 21, 25, 21, 30, 31, 30, 30, 30, 30, 31, 30, 30, 30, 30, 30, 30, 21, 30, 26],
                    [26, 30, 31, 30, 30, 30, 30, 30, 30, 31, 30, 30, 30, 25, 30, 31, 31, 30, 30, 30, 26],
                    [26, 30, 30, 31, 30, 30, 30, 25, 30, 30, 30, 21, 30, 30, 30, 30, 30, 30, 30, 30, 26],
                    [26, 30, 30, 30, 30, 30, 30, 30, 31, 21, 30, 30, 31, 30, 30, 21, 30, 30, 31, 30, 26],
                    [26, 30, 31, 21, 30, 21, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 21, 26],
                    [26, 30, 31, 30, 31, 30, 21, 30, 30, 30, 30, 30, 30, 21, 30, 30, 30, 25, 30, 31, 26],
                    [26, 30, 30, 25, 30, 31, 30, 31, 30, 30, 25, 30, 31, 30, 30, 25, 32, 32, 29, 32, 26],
                    [27, 30, 30, 31, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 29, 30, 31, 30, 30, 27],
                    [27, 30, 30, 30, 30, 30, 31, 30, 30, 31, 30, 30, 31, 30, 30, 29, 30, 30, 30, 30, 27],
                    [27, 30, 31, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 29, 31, 30, 30, 30, 27],
                    [26, 30, 30, 30, 31, 30, 30, 25, 30, 30, 31, 30, 30, 31, 30, 25, 30, 31, 30, 31, 26],
                    [26, 31, 30, 30, 30, 30, 30, 31, 30, 30, 30, 30, 25, 30, 30, 25, 30, 30, 31, 30, 26],
                    [26, 32, 33, 32, 29, 29, 33, 32, 32, 30, 30, 30, 30, 30, 31, 25, 30, 25, 30, 31, 26],
                    [26, 30, 31, 30, 30, 30, 30, 30, 25, 30, 31, 30, 30, 30, 30, 25, 30, 30, 21, 30, 26],
                    [27, 30, 30, 21, 31, 30, 30, 30, 25, 32, 29, 33, 32, 33, 32, 32, 31, 30, 30, 31, 26],
                    [27, 30, 31, 30, 30, 30, 30, 30, 31, 30, 30, 25, 21, 30, 31, 30, 30, 31, 30, 30, 26],
                    [27, 31, 30, 25, 30, 21, 31, 30, 30, 30, 31, 30, 30, 30, 30, 21, 30, 30, 25, 30, 26],
                    [26, 30, 31, 30, 31, 30, 30, 30, 30, 21, 30, 30, 31, 30, 30, 30, 31, 21, 30, 31, 26],
                    [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26]],
                'mapa3': 
                    [[11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                    [11, 14, 14, 14, 13, 15, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 24, 14, 14, 14, 11],
                    [11, 14, 18, 13, 13, 13, 13, 13, 22, 13, 13, 13, 18, 13, 13, 22, 13, 13, 13, 14, 11],
                    [11, 14, 13, 22, 22, 13, 13, 18, 13, 13, 13, 13, 13, 13, 15, 13, 20, 13, 24, 14, 11],
                    [11, 24, 15, 13, 13, 13, 13, 13, 24, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 11],
                    [11, 13, 13, 13, 13, 13, 13, 13, 13, 13, 22, 13, 20, 13, 13, 13, 24, 13, 18, 13, 11],
                    [11, 13, 13, 13, 13, 22, 13, 13, 13, 13, 15, 13, 13, 13, 13, 22, 13, 13, 13, 13, 11],
                    [11, 17, 16, 23, 16, 17, 16, 23, 16, 17, 16, 17, 16, 23, 16, 17, 16, 23, 16, 17, 11],
                    [11, 13, 13, 13, 13, 13, 13, 13, 13, 13, 17, 13, 13, 13, 13, 13, 13, 22, 13, 13, 11],
                    [12, 13, 20, 13, 22, 13, 18, 18, 13, 13, 16, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12],
                    [12, 13, 13, 13, 13, 13, 22, 13, 13, 13, 23, 13, 13, 13, 15, 13, 13, 13, 13, 13, 12],
                    [12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 23, 13, 13, 13, 13, 22, 13, 18, 13, 13, 12],
                    [11, 13, 13, 13, 22, 13, 13, 13, 22, 13, 17, 13, 13, 13, 13, 13, 13, 13, 22, 13, 11],
                    [11, 13, 22, 13, 13, 13, 13, 13, 15, 13, 16, 13, 13, 13, 13, 13, 13, 24, 13, 13, 11],
                    [11, 13, 13, 13, 13, 13, 22, 13, 13, 13, 17, 13, 13, 13, 13, 20, 13, 13, 13, 13, 11],
                    [11, 13, 24, 13, 15, 13, 13, 13, 13, 13, 16, 24, 13, 22, 13, 13, 22, 13, 13, 13, 11],
                    [11, 13, 22, 13, 22, 13, 22, 13, 20, 13, 17, 13, 13, 24, 13, 13, 13, 13, 13, 13, 11],
                    [11, 14, 13, 13, 13, 13, 13, 13, 13, 13, 23, 13, 13, 13, 13, 13, 13, 24, 13, 14, 11],
                    [11, 14, 13, 24, 13, 13, 13, 13, 13, 22, 17, 13, 13, 22, 13, 13, 18, 13, 13, 14, 11],
                    [11, 14, 14, 14, 13, 20, 13, 13, 13, 13, 16, 13, 13, 13, 13, 15, 13, 14, 14, 14, 11],
                    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]],
                    }


        # matriz 21x21 de um exemplo de mapa
        self.map = self.mapas[chave]                        

        # dicionário com as informações de cada tile diferente (imagem e tipo, vamos usar o tipo para calcualr colisão)
        self.tiles = {0: {'sprite': pg.transform.scale(pg.image.load('images/grass.png'), (32,32)), 'type': 'chao'},
                      1: {'sprite': pg.transform.scale(pg.image.load('images/tree.png'), (32,32)), 'type': 'parede'},
                      2: {'sprite': pg.transform.scale(pg.image.load('images/grass2.png'), (32,32)), 'type': 'spawn'},
                      3: {'sprite': pg.transform.scale(pg.image.load('images/tree2.png'), (32,32)), 'type': 'parede'},
                      4: {'sprite': pg.transform.scale(pg.image.load('images/grass3.png'), (32,32)), 'type': 'chao'},
                      5: {'sprite': pg.transform.scale(pg.image.load('images/rio g1.png'), (32,32)), 'type': 'passar'},
                      6: {'sprite': pg.transform.scale(pg.image.load('images/toco.png'), (32,32)), 'type': 'passar'},
                      7: {'sprite': pg.transform.scale(pg.image.load('images/flor.png'), (32,32)), 'type': 'chao'},
                      8: {'sprite': pg.transform.scale(pg.image.load('images/rio g2.png'), (32,32)), 'type': 'passar'},
                      9: {'sprite': pg.transform.scale(pg.image.load('images/madeira.png'), (32,32)), 'type': 'chao'},
                      10: {'sprite': pg.transform.scale(pg.image.load('images/madeira2.png'), (32,32)), 'type': 'parede'},
                      11: {'sprite': pg.transform.scale(pg.image.load('images/piso ci5.png'), (32,32)), 'type': 'parede'},
                      12: {'sprite': pg.transform.scale(pg.image.load('images/piso ci4.png'), (32,32)), 'type': 'spawn'},
                      13: {'sprite': pg.transform.scale(pg.image.load('images/piso ci7.png'), (32,32)), 'type': 'chao'},
                      14: {'sprite': pg.transform.scale(pg.image.load('images/piso ci3.png'), (32,32)), 'type': 'parede'},
                      15: {'sprite': pg.transform.scale(pg.image.load('images/fantasma.png'), (32,32)), 'type': 'passar'},
                      16: {'sprite': pg.transform.scale(pg.image.load('images/rio ci1.png'), (32,32)), 'type': 'passar'},
                      17: {'sprite': pg.transform.scale(pg.image.load('images/rio ci2.png'), (32,32)), 'type': 'passar'},
                      18: {'sprite': pg.transform.scale(pg.image.load('images/porta ci.png'), (32,32)), 'type': 'passar'},
                      19: {'sprite': pg.transform.scale(pg.image.load('images/rio ci1.png'), (32,32)), 'type': 'passar'},
                      20: {'sprite': pg.transform.scale(pg.image.load('images/caveira.png'), (32,32)), 'type': 'parede'},
                      21: {'sprite': pg.transform.scale(pg.image.load('images/troncos.png'), (32,32)), 'type': 'parede'},
                      22: {'sprite': pg.transform.scale(pg.image.load('images/piso ci2.png'), (32,32)), 'type': 'chao'},
                      23: {'sprite': pg.transform.scale(pg.image.load('images/piso ci6.png'), (32,32)), 'type': 'chao'},
                      24: {'sprite': pg.transform.scale(pg.image.load('images/tumulo.png'), (32,32)), 'type': 'parede'},
                      25: {'sprite': pg.transform.scale(pg.image.load('images/arbusto2.png'), (32,32)), 'type': 'parede'},
                      26: {'sprite': pg.transform.scale(pg.image.load('images/arbusto1.png'), (32,32)), 'type': 'parede'},
                      27: {'sprite': pg.transform.scale(pg.image.load('images/piso de1.png'), (32,32)), 'type': 'spawn'},
                      28: {'sprite': pg.transform.scale(pg.image.load('images/piso de2.png'), (32,32)), 'type': 'chao'},
                      29: {'sprite': pg.transform.scale(pg.image.load('images/piso de3.png'), (32,32)), 'type': 'chao'},
                      30: {'sprite': pg.transform.scale(pg.image.load('images/piso de4.png'), (32,32)), 'type': 'chao'},
                      31: {'sprite': pg.transform.scale(pg.image.load('images/piso de5.png'), (32,32)), 'type': 'chao'},
                      32: {'sprite': pg.transform.scale(pg.image.load('images/rio de1.png'), (32,32)), 'type': 'passar'},
                      33: {'sprite': pg.transform.scale(pg.image.load('images/rio de2.png'), (32,32)), 'type': 'passar'}}
    
    # Desenha o mapa
    def draw(self):
        # Caminha por todos os números da matriz e desenha a imagem correspondente nas cordenadas correspondentes
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                self.win.blit(self.tiles[self.map[j][i]]['sprite'], (self.x+32*i, self.y+32*j))