import pygame as pg
import math

# initialize Pygame
pg.init()

######################################################################################################
# classe responsavel pelos prejeteis do jogo, no momento somente o jogador consegue criar projeteis  #
######################################################################################################
class projectile(object):
    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT, direction):
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
        self.img = pg.image.load('images/bullet.png')

        # direção é a chave para os sen e cos dessa bala
        self.direction = direction
        # angles é um dicionario com os senos e cosenos de cada angulo de 0 a 365 de 5 em 5
        self.angles = {0: [0.0, 1.0], 5: [0.087, 0.996], 10: [0.174, 0.985], 15: [0.259, 0.966], 20: [0.342, 0.94], 25: [0.423, 0.906], 30: [0.5, 0.866], 35: [0.574, 0.819], 40: [0.643, 0.766], 45: [0.707, 0.707], 50: [0.766, 0.643], 55: [0.819, 0.574], 60: [0.866, 0.5], 65: [0.906, 0.423], 70: [0.94, 0.342], 75: [0.966, 0.259], 80: [0.985, 0.174], 85: [0.996, 0.087], 90: [1.0, 0.0], 95: [0.996, -0.087], 100: [0.985, -0.174], 105: [0.966, -0.259], 110: [0.94, -0.342], 115: [0.906, -0.423], 120: [0.866, -0.5], 125: [0.819, -0.574], 130: [0.766, -0.643], 135: [0.707, -0.707], 140: [0.643, -0.766], 145: [0.574, -0.819], 150: [0.5, -0.866], 155: [0.423, -0.906], 160: [0.342, -0.94], 165: [0.259, -0.966], 170: [0.174, -0.985], 175: [0.087, -0.996], 180: [0.0, -1.0], 185: [-0.087, -0.996], 190: [-0.174, -0.985], 195: [-0.259, -0.966], 200: [-0.342, -0.94], 205: [-0.423, -0.906], 210: [-0.5, -0.866], 215: [-0.574, -0.819], 220: [-0.643, -0.766], 225: [-0.707, -0.707], 230: [-0.766, -0.643], 235: [-0.819, -0.574], 240: [-0.866, -0.5], 245: [-0.906, -0.423], 250: [-0.94, -0.342], 255: [-0.966, -0.259], 260: [-0.985, -0.174], 265: [-0.996, -0.087], 270: [-1.0, -0.0], 275: [-0.996, 0.087], 280: [-0.985, 0.174], 285: [-0.966, 0.259], 290: [-0.94, 0.342], 295: [-0.906, 0.423], 300: [-0.866, 0.5], 305: [-0.819, 0.574], 310: [-0.766, 0.643], 315: [-0.707, 0.707], 320: [-0.643, 0.766], 325: [-0.574, 0.819], 330: [-0.5, 0.866], 335: [-0.423, 0.906], 340: [-0.342, 0.94], 345: [-0.259, 0.966], 350: [-0.174, 0.985], 355: [-0.087, 0.996]}
    
    def update(self, dt):
        # para permitir criar balas em novos angulos que não fazem parte do dicionário
        if not(self.direction in self.angles):
            angle = self.direction*math.pi/180
            # adiciona esse novo angulo ao dicionario para só chamar math.sin e math.cos uma vez por nova bala
            self.angles[self.direction] = [round(math.sin(angle),3), round(math.cos(angle),3)]

        # calcula a velocidade x e y com base nos senos e cosenos (eixo y é invertido no pygame, multiplicamos por -1)
        speedX = self.vel*self.angles[self.direction][1]*dt
        speedY = -self.vel*self.angles[self.direction][0]*dt


        # calcula a nova posição da bala   
        self.x += speedX
        self.y += speedY

    # desenha essa bala
    def draw(self):
        self.win.blit(self.img, (self.x, self.y))
