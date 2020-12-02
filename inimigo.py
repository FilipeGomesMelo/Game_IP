import pygame
from math import atan2, degrees, pi
import math
from random import seed, random
from datetime import datetime

# inicializa pygame
pygame.init()

#############################################################################################
#   Essa é a classe dos inimigos, ela cria o inimigo em um bloco de spawn aleatório         #
#   e move ele em linha reta na direção do jogador                                          #
#############################################################################################
class inimigo(object):
    # inicializa o inimigo
    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT,mapa):
        # cria uma seed para escolher o ponto de spawn aleatório
        seed(datetime.now())

        # essa é a lista onde vamos colocar todos os pontos de spawn possiveis
        cordenadas = []

        # spawn dos inimigos, vamos passar por todo o mapa atual e salvar as cordenadas de tiles do tipo spawn
        for i in range(len(mapa.map)):
            for j in range(len(mapa.map)):
                if mapa.tiles[mapa.map[j][i]]["type"] == "spawn":
                    cordenadas.append([j*32, i*32])

        # posição x e y do tile selecionado na tela
        posicao = cordenadas[round(random()*100)% len(cordenadas)]

        # usa a posição para determinar as cordenadas em que o inimigo vai nascer
        self.x = posicao[1]
        self.y = posicao[0]

        # largura e altura do inimigo
        self.width = width
        self.height = height

        # janela em que o inimigo vai ser desenhado e suas dimenções
        self.win = window
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        # imagem do inimigo
        self.img = pygame.transform.scale(pygame.image.load('images/inimigo.png'), (self.width, self.height))

        # velocidade do inimigo
        self.vel = 0.10

    # desenha o inimigo na tela
    def draw(self):
        self.win.blit(self.img, (self.x, self.y))

    # essa função é essencialmente a mesma que a função do mesmo nome na classe jogador
    # dessa vez, inimigos podem andar em tiles do tipo spawn e chão e não podem andar em tiles do tipo parede e passar
    def maior_movimento_valido(self, dt, mapa, speedX, speedY):
        # a representa a diferença entre o tamanho real do sprite do jogador e da "hitbox" com o mapa
        # isso serve para cirar uma janela de pixels maior para passar por espaços pequenos de um tile
        a = 2

        # corners salva os extremos da "hitbox"
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # move o inimigo somente se a posição final for em um bloco tipo 'chão'
        # basicamente, se eu for me mover para uma posição e essa posição não for válida, eu tento dnv com um px a menos
        # até encontrar uma posição em que eu possa me mover
        if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((corners[0][1]+speedX*dt)//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((corners[1][1]+speedX*dt)//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((corners[2][1]+speedX*dt)//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((corners[3][1]+speedX*dt)//32)%21]]['type'] not in ['parede', 'passar']:
            self.x += speedX*dt
        else:
            # se a soma da posição velocidade for um tile que o jogador não deveria conseguir entrar, então
            # esses loops vão procurar o maior movimeno possível na direção dada pela velocidade
            if speedX < 0:
                x = self.x + speedX*dt
                while(x < self.x):
                    if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((x+a)//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((x+a)//32)%21]]['type'] not in ['parede', 'passar']:
                        self.x = x
                        break
                    x+=1
            if speedX > 0:
                x = self.x + speedX*dt
                while(self.x < x):
                    if mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] not in ['parede', 'passar']:
                        self.x = x
                        break
                    x-=1
        
        # atualiza corners agora que movemos o personagem no eixo x
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # mesma coisa que foi feita com o eixo x
        if mapa.tiles[mapa.map[int((corners[0][0]+speedY*dt)//32)%21][int((corners[0][1])//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[1][0]+speedY*dt)//32)%21][int((corners[1][1])//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[2][0]+speedY*dt)//32)%21][int((corners[2][1])//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((corners[3][0]+speedY*dt)//32)%21][int((corners[3][1])//32)%21]]['type'] not in ['parede', 'passar']:
            self.y += speedY*dt
        else:
            # Mesma coisa que foi feita com a velocidade x
            if speedY < 0:
                y = self.y + speedY*dt
                while(y < self.y):
                    if mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[0][1])//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[1][1])//32)%21]]['type'] not in ['parede', 'passar']:
                        self.y = y
                        break
                    y += 1
            if speedY > 0:
                y = self.y + speedY*dt
                while(y > self.y):
                    if mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[2][1])//32)%21]]['type'] not in ['parede', 'passar'] and mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[3][1])//32)%21]]['type'] not in ['parede', 'passar']:
                        self.y = y
                        break
                    y -= 1

    # faz update nesse inimigo, basicamente só faz ele se mover na direção do jogador
    def update(self, x, y, dt, mapa):
        # se a função recebe -1 e -1 como x e y, o inimigo não se move, isso é usado para o item relógio
        if x != -1 and y != -1:
            # variação de x e variação de y da posição do inimigo e a posição do jogador, vamos usar para calcular o ângulo
            dx = x - self.x
            dy = y - self.y
            
            # calcula o angulo em radianos e coloca esse angulo na janela de 0~2*pi
            rads = atan2(dy, dx)
            rads %= 2 * pi
            
            # calcula a velocidade do inimigo em cada eixo baseado no angulo em radianos
            speedX = self.vel * round(math.cos(rads), 3)
            speedY = self.vel * round(math.sin(rads), 3)
        else:
            # não move enquanto o item relógio está ativado
            speedX = 0
            speedY = 0

        # calcula o maior movimento válido
        self.maior_movimento_valido(dt, mapa, speedX, speedY)
