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

items = []

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
        if dt_enemy > 1000:
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

        for item in items:
            item.update(t)
            col = item.player_colision(king)
            if col != -1 and col != 'S_coin':
                collected_itens[col] += 1
                print(collected_itens)
            if col == 'S_coin':
                collected_itens['coin'] += 10
                print(collected_itens)
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
            if item.existes == False:
                items.pop(items.index(item))

        # king.check_enemy(zombies)
                
        # update do inimigo
        for zombie in zombies:
            zombie.update(king.x, king.y, dt, mapa)

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

    for item in items:
        item.draw()

    # desenha o jogador e as suas balas 
    king.draw()

    # faz update da tela
    pg.display.update()

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