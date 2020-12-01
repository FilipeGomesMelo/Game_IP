import pygame as pg
import player as pl
import mapa as mp
import inimigo as ini
import items as it
from random import seed, random

# initialize Pygame
pg.init()
seed(random())

#Música_de_Fundo
pg.mixer.init()
pg.mixer.music.load("sounds/song.mp3")
pg.mixer.music.set_volume(0.7)
pg.mixer.music.play(-1)

# sound effects
damage_sound = pg.mixer.Sound("sounds/hurt.wav")
walk_sound = pg.mixer.Sound("sounds/walk_grass.wav")
projectile_hit_wall = pg.mixer.Sound("sounds/projectile_wall.wav")
enemy_death = pg.mixer.Sound("sounds/enemy_dies.wav")

# dimenções da janela
WINDOW_WIDTH = 672
WINDOW_HEIGHT = 672

# setup da tela
win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Unitled Wizard Game")

# setup icone da tela
icon = pg.image.load('images/wizard.png')
pg.display.set_icon(icon)

# cria o jogador no centro da tela
king = pl.player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)

# cria o mapa
mapa = mp.mapa(0, 0, win)

# cria lista que vai guardar todos inimigos
zombies = []

# cria a lista que guarda todos os itens
items = []

# dicionário que salva a quantidade de cada itens coletados
collected_itens = {'coin': 0,
                    'boots': 0,
                    'coffee': 0,
                    'multi_shot': 0,
                    'fast_shot': 0,
                    'clock': 0}

# roda o jogo
def main():
    ticks_last_frame = 0
    ticks_last_enemy = -2000


    # mude para true para ver o fps
    show_fps = True
    if show_fps:
        font = pg.font.Font(None, 30)
        clock = pg.time.Clock()
    
    # loop infinito que roda o jogo
    while True:
        # permite fechar a janela
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        # fechar a janela apretando esc
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()

        # Calcula delta time, usado pra fazer o movimento continuo
        t = pg.time.get_ticks()
        dt = (t - ticks_last_frame)
        ticks_last_frame = t

        # responsavel por spawnar os inimigos
        dt_enemy = t - ticks_last_enemy
        if dt_enemy > 1000 and king.active_item['clock'] == -1:
            zombies.append(ini.inimigo(0, WINDOW_HEIGHT // 2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT))
            ticks_last_enemy = t

        # update o jogador e as balas
        king.update(dt, mapa)
        if king.health <= 0:
            reset_all()
        for bullet in king.bullets:
            killed = bullet.check_enemy(zombies)
            if killed != -1:
                enemy_death.play()
                zombies.pop(zombies.index(killed))
                rand = round((random()*1000)%65)
                if 0 <= rand < 65:
                    items.append(it.item(killed.x, killed.y, win, rand, t))

        # updates todos itens
        for item in items:
            item.update(t)
            # checa por itens coletados e adiciona eles no dicionário
            col = item.player_colision(king)
            if col != -1 and col != 'S_coin':
                collected_itens[col] += 1
            if col == 'S_coin':
                collected_itens['coin'] += 10
            elif col == 'boots':
                if king.vel <= 0.35:
                    king.vel *= 1.05
                    king.d_vel *= 1.05
                if king.vel > 0.35:
                    king.vel = 0.35
                    king.d_vel = 0.35/(2**(1/2))
            elif col == 'coffee':
                if king.shot_cooldown_normal >= 300:
                    king.shot_cooldown_normal *= 0.90
                if king.shot_cooldown_normal < 300: 
                    king.shot_cooldown_normal = 300
            elif col in ['multi_shot', 'fast_shot', 'clock', 'wheel'] and king.current_item == None:
                king.current_item = col
            else:
                king.active_item[col] = t


            if item.existes == False:
                items.pop(items.index(item))
        print(king.current_item)        
        # update do inimigo
        for zombie in zombies:
            if king.active_item['clock'] != -1 and t-king.active_item['clock'] < king.item_duration:
                zombie.update(-1, -1, dt, mapa)
            else:
                zombie.update(king.x, king.y, dt, mapa)

        if t-king.active_item['clock'] > king.item_duration:
            king.active_item['clock'] = -1

        # checa se algum inimigo está tocando o jogador e toca o som de dano
        if king.check_enemy(zombies, t):
            damage_sound.play()

        # desenha tudo 
        draw_all()

        # mostra o fps do jogo
        if show_fps:
            fps = font.render(str(int(clock.get_fps())), True, pg.Color('White'))
            win.blit(fps, (50, 50))
            pg.display.flip()
            clock.tick(120)

        # update diplay
        pg.display.update()


#  desenha tudo
def draw_all():
    # desenha o mapa
    mapa.draw()

    #desenhar inimigos
    for zombie in zombies:
        zombie.draw()

    # desenha os itens
    for item in items:
        item.draw()

    # desenha o jogador e as suas balas 
    king.draw()

    # faz update da tela
    pg.display.update()

# reseta o jogo
def reset_all():
    global king 
    king = pl.player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)
    global zombies
    zombies = []
    global items 
    items = []

    global collected_itens
    collected_itens = {'coin': 0,
                        'boots': 0,
                        'coffee': 0,
                        'multi_shot': 0,
                        'fast_shot': 0,
                        'clock': 0}

main()