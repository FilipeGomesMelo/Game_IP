import pygame as pg
import math

# initialize Pygame
pg.init()

######################################################################################################
# classe responsavel pelos prejeteis do jogo, no momento somente o jogador consegue criar projeteis  #
######################################################################################################
class projectile(object):
    # inicializa o priojétil
    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT, direction):
        # define se a bala existe ou não
        self.existe = 1

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
        self.img = pg.transform.scale(pg.image.load('images/spark2.png'), (self.width,self.height))

        # direção é a chave para os sen e cos dessa bala
        self.direction = direction
        # angles é um dicionario com os senos e cosenos de cada angulo de 0 a 365 de 5 em 5
        self.angles = {}

    # basicamente a mesma coisa de todas as outras colisões (jogador-inimigo e item-jogador)
    def check_enemy(self, enemies):
        # quatro cantos da bala
        corners = [[self.x, self.y], [self.x+self.width, self.y], [self.x, self.y+self.height], [self.x+self.width, self.y+self.height]]
        
        # passa por toda a lista de inimigos
        for enemy in enemies:
            # se qualquer um dos cantos da bala está dentro do inimigo, então retorna o inimigo que está tocando
            for corner in corners:
                if enemy.x+1 <= corner[0] <= enemy.x + enemy.width and enemy.y <= corner[1] <= enemy.y + enemy.height:
                    self.existe = -1
                    return enemy
        # se não está tocando em nenhum inimigo, retorna -1
        return -1

    # faz update da bala
    def update(self, dt, mapa):
        # para permitir criar balas em novos angulos que não fazem parte do dicionário
    
        # calcula o angulo em rads, transformar de radianos para graus para radianos novamente é ineficiente,
        # mas como isso torna mais intuitivo para a mira com as setas e o jogo roda bem e isso não parece estar causando
        # nenhum problema, é o que vamos fazer
        angle = self.direction*math.pi/180

        # calcula a velocidade x e y com base nos senos e cosenos (eixo y é invertido no pygame, multiplicamos por -1)
        speedX = self.vel*round(math.cos(angle),3)*dt
        # re-inverte o angulo
        speedY = -self.vel*round(math.sin(angle),3)*dt


        # calcula a nova posição da bala   
        self.x += speedX
        self.y += speedY

        # garante que a bala não sai da tela
        if not(0 < self.x < self.WINDOW_WIDTH and 0 < self.y < self.WINDOW_HEIGHT) or not(0 < self.x + self.width < self.WINDOW_WIDTH and 0 < self.y < self.WINDOW_HEIGHT):
            self.existe = 0
        if self.existe:
            if mapa.tiles[mapa.map[int(self.y//32)%21][int(self.x//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'parede' or mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x)//32)%21]]['type'] == 'parede':
                self.existe = 0

    # desenha essa bala
    def draw(self):
        self.win.blit(self.img, (self.x, self.y))
