import pygame as pg
import projectile as proj

# initialize Pygame
pg.init()

#############################################################################################
#   Essa é a classe player, ela faz tudo relacionado ao jogador (movimento, vida itens etc) #
#   A classe jogador também cria e faz update das balas pela lista de objetos self.bullet   #
#############################################################################################


class player(object):
    def __init__(self, x, y, width, height, window, WINDOW_WIDTH, WINDOW_HEIGHT):
        # posição x e y do jogador no mapa
        self.x = x
        self.y = y

        # largura e altura do jogador
        self.width = width
        self.height = height

        # velocidade linear do jogador e as projeções dessa velocidade no eixo x e y para quando ele se move em 45º
        self.vel = 0.25
        self.d_vel = self.vel/(2**(1/2))

        # quanto tempo passou desde o ultimo tiro e quanto tempo até ele poder atirar novamente
        self.ticks_last_shot = 0
        self.shot_cooldown = 250
        self.shot_cooldown_normal = self.shot_cooldown

        # janela em que o jogador vai ser desenhado e suas dimenções
        self.win = window
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        # sprites do jogador
        self.img = pg.image.load('images/cowboy_idle.png')

        # lista de objetos projectile (balas)
        self.bullets = []

        # quais armas estão ativas no momento para controlar seus efeitos e permitir que funcionam de forma acumulativo
        self.gun_active = {'shot': False, 'machine': False, 'wheel': False}

    # responsavel por calcular e controlar o movimento do jogador
    def calculate_speed(self, keys):
        speedX = 0
        speedY = 0

        # o jogador pode se mover em 8 direções ao todo, cima, baixo, esquerda, direita e as diagonais correspondentes
        if keys[pg.K_a]:
            if keys[pg.K_w]:
                speedX = -self.d_vel
                speedY = -self.d_vel
            elif keys[pg.K_s]:
                speedX = -self.d_vel
                speedY = self.d_vel
            else:
                speedX = -self.vel
        elif keys[pg.K_d]:
            if keys[pg.K_w]:
                speedX = self.d_vel
                speedY = -self.d_vel
            elif keys[pg.K_s]:
                speedX = self.d_vel
                speedY = self.d_vel
            else:
                speedX = self.vel
        elif keys[pg.K_s]:
            speedY = self.vel
        elif keys[pg.K_w]:
            speedY = -self.vel
        
        # garante que o jogador não sai dos limites da tela jogavel    
        if (self.x <= 0 and speedX < 0):
            speedX = 0
            self.x = 0
        elif (self.x >= self.WINDOW_WIDTH-self.width and speedX > 0):
            speedX = 0
            self.x = self.WINDOW_WIDTH-self.width
        if (self.y <= 0 and speedY < 0):
            speedY = 0
            self.y = 0
        elif (self.y >= self.WINDOW_HEIGHT-self.height and speedY > 0):
            speedY = 0
            self.y = self.WINDOW_HEIGHT-self.height
        
        # retorna as velocidades do jogador no eixo X e Y para calcular a sua nova posição
        return speedX, speedY
    
    # controla a mira e gera novas balas
    def new_bullets(self, keys):
        # esse vetor corresponde as direções de todas as balas que vamos criar
        direction = []
        
        # calcula o tempo desde o ultimo tiro
        t = pg.time.get_ticks()
        dt_shot = (t - self.ticks_last_shot)   
        
        # se o tempo desde o ultimo tiro for maior que o cool down, o jogador pode atirar
        if dt_shot >= self.shot_cooldown:

            # essa parte é usada para ativar as diferentes armas, é apenas para debug e é temporaria
            if keys[pg.K_h]:
                self.gun_active = {'shot': False, 'machine': False, 'wheel': False}
                self.ticks_last_shot = t
            elif keys[pg.K_j]:
                if self.gun_active['shot']:
                    self.gun_active['shot'] = False
                else:
                    self.gun_active['shot'] = True
                self.ticks_last_shot = t
            elif keys[pg.K_k]:
                if self.gun_active['machine']:
                    self.gun_active['machine'] = False
                else:
                    self.gun_active['machine'] = True
                self.ticks_last_shot = t
            elif keys[pg.K_l]:
                if self.gun_active['wheel']:
                    self.gun_active['wheel'] = False
                else:
                    self.gun_active['wheel'] = True
                self.ticks_last_shot = t

            # se a arma "wheel" estiver ativa, vamos gerar uma bala em todas as 8 direções principais
            if self.gun_active['wheel']:
                if keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_UP] or keys[pg.K_DOWN]:
                    for i in range(0,360,45):
                        direction.append(i)
                    self.ticks_last_shot = t
            # caso contrario vamos ver em que direção o jogador está mirando e adicionar essa direção na lista
            else:
                if keys[pg.K_LEFT]:
                    if keys[pg.K_UP]:
                        direction.append(135)
                    elif keys[pg.K_DOWN]:
                        direction.append(225)
                    else:
                        direction.append(180)
                    self.ticks_last_shot = t
                elif keys[pg.K_RIGHT]:
                    if keys[pg.K_UP]:
                        direction.append(45)
                    elif keys[pg.K_DOWN]:
                        direction.append(315)
                    else:
                        direction.append(0)
                    self.ticks_last_shot = t
                elif keys[pg.K_UP]:
                    self.ticks_last_shot = t
                    direction.append(90)
                elif keys[pg.K_DOWN]:
                    self.ticks_last_shot = t
                    direction.append(270)
            
            # se a shot_gun estiver ativa, colocaremos mais duas balas, a +15º e a -15º de cada bala já existente
            if self.gun_active['shot']:
                for i in range(len(direction)):
                    direction.append((direction[i]-15)%360)
                    direction.append((direction[i]+15)%360)
        
        # adiciona as balas novas nas direções dadas a lista
        self.add_bullets(direction)
        # deleta as balas que sairam da tela
        self.del_bullets()
    

    # adiciona as balas nas direções selecionadas
    def add_bullets(self, direction):
        for i in direction:
            self.bullets.append(proj.projectile(self.x+self.width/2, self.y+self.height/2, 10, 10, self.win, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, i))
    
    # deleta todas as balas que não estão mais na tela
    def del_bullets(self):
        for bullet in self.bullets:
            if not(0 < bullet.x < self.WINDOW_WIDTH and 0 < bullet.y < self.WINDOW_HEIGHT):
                self.bullets.pop(self.bullets.index(bullet))

    # controla o movimento do jogador
    def control(self, dt):
        # teclas precionadas
        keys = pg.key.get_pressed()   

        # ajusta a velocidade do cooldown das balas, temporaria, fazer função propria para isso quando possível    
        if self.gun_active['machine']:
            self.shot_cooldown = self.shot_cooldown_normal/1.5
        else:
            self.shot_cooldown = self.shot_cooldown_normal
        
        # chama calculate_speed para calcular as velocidades x e y do jogador
        speedX, speedY = self.calculate_speed(keys)

        # move o jogador    
        self.x += speedX*dt
        self.y += speedY*dt

        # chama a função responsavel por fazer os tiros do jogador
        self.new_bullets(keys)

    # desenha as balas e depois o jogador por cima delas
    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        self.win.blit(self.img, (self.x, self.y))

    # updata o jogador e as balas
    def update(self, dt):
        self.control(dt) 
        for bullet in self.bullets:
            bullet.update(dt)
