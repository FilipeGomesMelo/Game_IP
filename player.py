import pygame as pg
import projectile as proj
from math import atan2, degrees, pi

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
        self.shot_cooldown = 500
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
        
        # coordenadas mouse
        self.mouseX = self.x
        self.mouseY = self.y

        # O plano é usar isso para poder facilitar a detecção de colisão, uma série de tuplas
        # que vai ser atualizada todo update
        self.corners = ((self.x, self.y), (self.x+self.width,self.y), (self.x,self.y+self.height), (self.x+self.width,self.y+self.height))


    # responsavel por calcular e controlar o movimento do jogador
    def calculate_speed(self, keys, mapa):
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
        if speedX < 0 and self.x <= 0:
            speedX = 0
        elif (self.x >= self.WINDOW_WIDTH-self.width and speedX > 0):
            speedX = 0
        if (self.y <= 0 and speedY < 0):
            speedY = 0
        elif (self.y >= self.WINDOW_HEIGHT-self.height and speedY > 0):
            speedY = 0
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
                
                # atirar utilizando o mouse enquanto wheel esta ativa
                if pg.mouse.get_pressed()[0]:
                    self.mouseX, self.mouseY = pg.mouse.get_pos()
                    dx = (self.x+self.width/2) - (self.mouseX-5)
                    dy = (self.y+self.height/2) - (self.mouseY-5)
                    rads = atan2(dy,-dx)
                    rads %= 2*pi
                    degs = round(degrees(rads), 3)
                    direction.append(degs)
                    for i in range(0,360, 45):
                        direction.append((degs+i)%360)
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

            # atirar com o mouse, somente quando wheel nn está ativa para evitar criar balas duplicadas
            # pg.mouse.get_pressed()[0] é true quando o jogador está segurando o botão esquerdo do mouse
            # [1] e [2] é o botão do meio e da direita respectivamente
            if pg.mouse.get_pressed()[0] and not(self.gun_active['wheel']):
                # salva as cordenadas x e y do mouse
                self.mouseX, self.mouseY = pg.mouse.get_pos()
                # encontra a "distância" do ponto de spawn das balas do jogador pro o mouse
                dx = (self.mouseX-5) - (self.x+self.width/2)
                dy = (self.mouseY-5) - (self.y+self.height/2)

                # calcula o angulo em graus
                rads = atan2(-dy, dx)
                rads %= 2*pi
                degs = round(degrees(rads))

                # salva esse angulo nas direções para poder cirar as balas
                direction.append(degs)

                # reseta o timer de shot cooldown
                self.ticks_last_shot = t
            
            # se a shot_gun estiver ativa, colocaremos mais duas balas, a +15º e a -15º de cada bala já existente
            if self.gun_active['shot']:
                for i in range(len(direction)):
                    direction.append((direction[i]-15)%360)
                    direction.append((direction[i]+15)%360)
              

        # adiciona as balas novas nas direções dadas a lista
        self.add_bullets(direction)
    

    # adiciona as balas nas direções selecionadas
    def add_bullets(self, direction):
        for i in direction:
            self.bullets.append(proj.projectile(self.x+self.width/2, self.y+self.height/2, 10, 10, self.win, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, i))

    # controla o movimento do jogador
    def control(self, dt, mapa):
        # teclas precionadas
        keys = pg.key.get_pressed()   

        # ajusta a velocidade do cooldown das balas, temporaria, fazer função propria para isso quando possível    
        if self.gun_active['machine']:
            self.shot_cooldown = self.shot_cooldown_normal/2
        else:
            self.shot_cooldown = self.shot_cooldown_normal
        
        # chama calculate_speed para calcular as velocidades x e y do jogador
        speedX, speedY = self.calculate_speed(keys, mapa)

        # move o jogador somente se a posição final for em um bloco tipo 'chão'
        # basicamente, se eu for me mover para uma posição e essa posição não for válida, eu tento dnv com um px a menos
        # até encontrar uma posição em que eu possa me mover
        if mapa.tiles[mapa.map[int((self.y)//32)%21][int((self.x+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y)//32)%21][int((self.x+self.width+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((self.x+self.width+speedX*dt)//32)%21]]['type'] == 'chao':
            self.x += speedX*dt
        else:
            # se a soma da posição velocidade for um tile que o jogador não deveria conseguir entrar, então
            # esses loops vão procurar o maior movimeno possível na direção dada pela velocidade
            if speedX < 0:
                x = self.x + speedX*dt
                while(x < self.x):
                    if mapa.tiles[mapa.map[int((self.y)//32)%21][int((x)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((x)//32)%21]]['type'] == 'chao':
                        self.x = x
                        break
                    x+=1
            if speedX > 0:
                x = self.x + speedX*dt
                while(self.x < x):
                    if mapa.tiles[mapa.map[int((self.y)//32)%21][int((x+self.width)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+self.height)//32)%21][int((x+self.width)//32)%21]]['type'] == 'chao':
                        self.x = x
                        break
                    x-=1
        if mapa.tiles[mapa.map[int((self.y+speedY*dt)//32)%21][int((self.x)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+speedY*dt)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+self.height+speedY*dt)//32)%21][int((self.x)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((self.y+speedY*dt+self.height)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'chao':
            self.y += speedY*dt
        else:
            # Mesma coisa que foi feita com a velocidade y
            if speedY < 0:
                y = self.y + speedY*dt
                while(y < self.y):
                    if mapa.tiles[mapa.map[int((y)//32)%21][int((self.x)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((y)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'chao':
                        self.y = y
                        break
                    y += 1
            if speedY > 0:
                y = self.y + speedY*dt
                while(y > self.y):
                    if mapa.tiles[mapa.map[int((y+self.height)//32)%21][int((self.x)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((y+self.height)//32)%21][int((self.x+self.width)//32)%21]]['type'] == 'chao':
                        self.y = y
                        break
                    y -= 1

        # garante que o jogador não sai dos limites da tela jogavel    
        if (self.x <= 0 and speedX < 0):
            self.x = 0
        elif (self.x >= self.WINDOW_WIDTH-self.width and speedX > 0):
            self.x = self.WINDOW_WIDTH-self.width
        if (self.y <= 0 and speedY < 0):
            self.y = 0
        elif (self.y >= self.WINDOW_HEIGHT-self.height and speedY > 0):
            self.y = self.WINDOW_HEIGHT-self.height 

        # chama a função responsavel por fazer os tiros do jogador
        self.new_bullets(keys)

    # desenha as balas e depois o jogador por cima delas
    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        self.win.blit(self.img, (self.x, self.y))

    # updata o jogador e as balas
    def update(self, dt, mapa):
        self.control(dt, mapa) 
        for bullet in self.bullets:
            if bullet.existe:
                bullet.update(dt, mapa)
            if not(bullet.existe):
                self.bullets.pop(self.bullets.index(bullet))