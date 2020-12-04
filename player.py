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

        # janela em que o jogador vai ser desenhado e suas dimensões
        self.win = window
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        # sprites do jogador
        self.img = pg.transform.scale(pg.image.load('images/wizard_idle2.png'), (32,36))

        # lista de objetos projectile (balas)
        self.bullets = []

        # quais armas estão ativas no momento para controlar seus efeitos e permitir que funcionam de forma acumulativo
        self.active_item = {'multi_shot': -1, 'fast_shot': -1, 'wheel': -1, 'clock': -1}
        
        # coordenadas mouse
        self.mouseX = self.x
        self.mouseY = self.y

        # i_frames é um bool que diz se os frames de invulnerável
        self.i_frames = False

        # tempo de duração dos frames de invulnerabilidade
        self.i_frames_duration = 1000

        # ticks da ultima vez que o jogador levou dano para calcular o tempo de frames de invulnerabilidade
        self.ticks_last_hit = 0

        # blink vai ser usado para 'piscar' o jogador quando este estiver invulnerável, mostrando ele frame sim e frame não
        self.blink = 0

        # som do projétil batendo em uma parede
        self.projectile_hit_wall = pg.mixer.Sound("sounds/projectile_wall.wav")

        # vida do jogador
        self.max_health = 3
        self.health = self.max_health

        # item atual do jogador
        self.current_item = None

        # tempo de duração do item
        self.item_duration = 10000

    # checa se o jogador está tocando um inimigo
    def check_enemy(self, enemies, t):

        # quatro cantos do jogador
        corners = [[self.x, self.y], [self.x+self.width, self.y], [self.x, self.y+self.height], [self.x+self.width, self.y+self.height]]
        # se o jogador não estiver invulnerável, vemos se o jogador está tocando em um inimigo
        if not self.i_frames:
            for enemy in enemies:
                for corner in corners:
                    if enemy.x+1 <= corner[0] <= enemy.x + enemy.width and enemy.y <= corner[1] <= enemy.y + enemy.height:
                        # reseta blink
                        self.blink = 0
                        # ativa frames de invulnerável
                        self.i_frames = True
                        # salva os ticks no momento do hit
                        self.ticks_last_hit = t
                        # takes damage
                        self.health -= 1
                        # interrompe a função
                        return True

        # se já se passou o tempo de duração dos frames de invulnerabilidade, desative a invunerabilidade
        elif t - self.ticks_last_hit > self.i_frames_duration:
            self.i_frames = False

    # responsavel por calcular e controlar o movimento do jogador
    def calculate_speed(self, keys):
        # velocidades em cada eixo
        speedX = 0
        speedY = 0

        # o jogador pode se mover em 8 direções ao todo, cima, baixo, esquerda, direita e as diagonais correspondentes
        x = (keys[pg.K_d] - keys[pg.K_a])
        y = (keys[pg.K_s] - keys[pg.K_w])

        # calcula a velocidade baseado nas teclas precionadas
        if x != 0 and y != 0:
            speedX = x*self.d_vel
            speedY = y*self.d_vel
        else:
            speedX = x*self.vel
            speedY = y*self.vel

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
            # se a arma "wheel" estiver ativa, vamos gerar uma bala em todas as 8 direções principais
            if self.active_item['wheel'] != -1 and t - self.active_item['wheel'] < self.item_duration:              
                # atirar utilizando o mouse enquanto wheel esta ativa
                if pg.mouse.get_pressed()[0]:
                    self.mouseX, self.mouseY = pg.mouse.get_pos()
                    dx = (self.mouseX-5) - (self.x+self.width/2)
                    dy = (self.mouseY-5) - (self.y+self.height/2)
                    rads = atan2(-dy,dx)
                    rads %= 2*pi
                    degs = round(degrees(rads), 3)
                    for i in range(0,360, 45):
                        direction.append((degs+i)%360)
                    self.ticks_last_shot = t
            # caso contrario vamos ver em que direção o jogador está mirando e adicionar essa direção na lista
            else:
                # atirar com o mouse, somente quando wheel nn está ativa para evitar criar balas duplicadas
                # pg.mouse.get_pressed()[0] é true quando o jogador está segurando o botão esquerdo do mouse
                # [1] e [2] é o botão do meio e da direita respectivamente
                if pg.mouse.get_pressed()[0]:
                    # salva as cordenadas x e y do mouse
                    self.mouseX, self.mouseY = pg.mouse.get_pos()
                    # encontra a "distância" do ponto de spawn das balas do jogador pro o mouse
                    dx = (self.mouseX-5) - (self.x+self.width/2)
                    dy = (self.mouseY-5) - (self.y+self.height/2)

                    # calcula o angulo em graus, eu inverto dy somente para tornar os angulos mais intuitivos no sentido convencional
                    rads = atan2(-dy, dx)
                    rads %= 2*pi
                    degs = round(degrees(rads))

                    # salva esse angulo nas direções para poder cirar as balas
                    direction.append(degs)

                    # reseta o timer de shot cooldown
                    self.ticks_last_shot = t
            
            # se a shot_gun estiver ativa, colocaremos mais duas balas, a +15º e a -15º de cada bala já existente
            if (self.active_item['multi_shot']) != -1 and (t - self.active_item['multi_shot'] < self.item_duration):
                for i in range(len(direction)):
                    direction.append((direction[i]-15)%360)
                    direction.append((direction[i]+15)%360)
            else:
                self.active_item['multi_shot'] = -1
              

        # adiciona as balas novas nas direções dadas a lista
        self.add_bullets(direction)
    

    # adiciona as balas nas direções selecionadas
    def add_bullets(self, direction):
        # usa as direções para criar novas balas
        for i in direction:
            self.bullets.append(proj.projectile(self.x+self.width/2, self.y+self.height/2, 12, 12, self.win, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, i))

    def maior_movimento_valido(self, dt, mapa, speedX, speedY):
        # a representa a diferença entre o tamanho real do sprite do jogador e da "hitbox" com o mapa
        # isso serve para cirar uma janela de px maior para passar por espaços pequenos de um tile
        a = 3

        # corners salva os extremos da "hitbox"
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # move o jogador somente se a posição final for em um bloco tipo 'chão'
        # basicamente, se eu for me mover para uma posição e essa posição não for válida, eu tento dnv com um px a menos
        # até encontrar uma posição em que eu possa me mover
        if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((corners[0][1]+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((corners[1][1]+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((corners[2][1]+speedX*dt)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((corners[3][1]+speedX*dt)//32)%21]]['type'] == 'chao':
            self.x += speedX*dt
        else:
            # se a soma da posição velocidade for um tile que o jogador não deveria conseguir entrar, então
            # esses loops vão procurar o maior movimeno possível na direção dada pela velocidade
            if speedX < 0:
                x = self.x + speedX*dt
                while(x < self.x):
                    if mapa.tiles[mapa.map[int((corners[0][0])//32)%21][int((x+a)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[2][0])//32)%21][int((x+a)//32)%21]]['type'] == 'chao':
                        self.x = x
                        break
                    x+=1
            if speedX > 0:
                x = self.x + speedX*dt
                while(self.x < x):
                    if mapa.tiles[mapa.map[int((corners[1][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[3][0])//32)%21][int((x+self.width-a)//32)%21]]['type'] == 'chao':
                        self.x = x
                        break
                    x-=1

        # atualiza corners agora que movemos o personagem no eixo x
        corners = [[self.y+a, self.x+a], [self.y+a, self.x+self.width-a], [self.y+self.height-a, self.x+a], [self.y+self.height-a, self.x+self.width-a]]

        # mesma coisa que foi feita com o eixo x
        if mapa.tiles[mapa.map[int((corners[0][0]+speedY*dt)//32)%21][int((corners[0][1])//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[1][0]+speedY*dt)//32)%21][int((corners[1][1])//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[2][0]+speedY*dt)//32)%21][int((corners[2][1])//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((corners[3][0]+speedY*dt)//32)%21][int((corners[3][1])//32)%21]]['type'] == 'chao':
            self.y += speedY*dt
        else:
            # Mesma coisa que foi feita com a velocidade x
            if speedY < 0:
                y = self.y + speedY*dt
                while(y < self.y):
                    if mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[0][1])//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((y+a)//32)%21][int((corners[1][1])//32)%21]]['type'] == 'chao':
                        self.y = y
                        break
                    y += 1
            if speedY > 0:
                y = self.y + speedY*dt
                while(y > self.y):
                    if mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[2][1])//32)%21]]['type'] == 'chao' and mapa.tiles[mapa.map[int((y+self.height-a)//32)%21][int((corners[3][1])//32)%21]]['type'] == 'chao':
                        self.y = y
                        break
                    y -= 1

    # controla o movimento do jogador
    def control(self, dt, mapa):
        # teclas precionadas
        keys = pg.key.get_pressed()   

        # ticks nesse momento
        t = pg.time.get_ticks()

        # ajusta a velocidade do cooldown das balas, temporaria, fazer função propria para isso quando possível    
        if (self.active_item['fast_shot'] != -1) and (t - self.active_item['fast_shot'] < self.item_duration):
            self.shot_cooldown = self.shot_cooldown_normal/2
        else:
            self.active_item['fast_shot'] = -1
            self.shot_cooldown = self.shot_cooldown_normal
        
        # ativa o item atual
        if keys[pg.K_SPACE] and self.current_item != None:
                self.active_item[self.current_item] = t
                self.current_item = None

        # chama calculate_speed para calcular as velocidades x e y do jogador
        speedX, speedY = self.calculate_speed(keys)

        # descobre o maior movimento "válido" do jogador, (movimento em que o jogador não entre em um tile que 
        # não deveria conseguir entrar), é uma gambiarra e definitivamente não é a melhor forma de fazer isso,
        # mas foi o que eu consegui
        self.maior_movimento_valido(dt, mapa, speedX, speedY)

        # chama a função responsavel por fazer os tiros do jogador
        self.new_bullets(keys)

    # desenha as balas e depois o jogador por cima delas
    def draw(self):
        # desenha as balas
        for bullet in self.bullets:
            bullet.draw()

        # se o jogador estiver invulnerável, ele ficara "piscando", sendo desenhado frame sim e frame não     
        if self.i_frames:
            # só desenha nos frames pares desde o frame em que o jogador levou o dano
            if self.blink % 2 == 0:
                self.blink += 1
                self.win.blit(self.img, (self.x, self.y))
            else:
                self.blink += 1
        # caso contrário, desenhe o jogador normalmente        
        else:
            self.win.blit(self.img, (self.x, self.y))

    # updata o jogador e as balas
    def update(self, dt, mapa):
        # controla o jogdor
        self.control(dt, mapa) 
        
        # update nas balas e remove as balas que não existem
        for bullet in self.bullets:
            if bullet.existe:
                bullet.update(dt, mapa)
            if not(bullet.existe):
                self.projectile_hit_wall.play()
                self.bullets.pop(self.bullets.index(bullet))
