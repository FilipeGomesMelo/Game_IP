import pygame as pg
import player as pl
import mapa as mp
import inimigo as ini
import items as it
from random import seed, random
from datetime import datetime

# inicializa o Pygame
pg.init()

# gera a seed que vamos usar no rng usando a data e hora que o jogo é aberto
seed(datetime.now())

# inicializa o mixer do pygame Música de fundo
pg.mixer.init()
# Música de fundo
pg.mixer.music.load("sounds/song.mp3")
pg.mixer.music.set_volume(0.7)
# coloca a música para tocar em loop 
pg.mixer.music.play(-1)

# efeitos sonoros
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
king = pl.player((WINDOW_WIDTH // 2)-16, (WINDOW_HEIGHT // 2)-16, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)

# cria o mapa
mapa = mp.mapa(0, 0, win, 'mapa1')

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

# salva a pontuação do jogador no último mapa
pontuacao_anterior = {'coin': 0}

# salva a pontuação do jogador nos 3 últimos mapas, reseta sempre que um ciclo novo começa
pontuacao_total = []

# imagem dos corações
heart_full = pg.transform.scale(pg.image.load('images/heart_full.png'), (30,30))
heart_empty = pg.transform.scale(pg.image.load('images/heart_empty.png'), (30,30))

# imagem da tela de começo de cada fase
press_start = pg.transform.scale(pg.image.load('images/press_start.png'), (98*3,14*3))

# caixa onde o item atual vai aparecer
canvas = pg.transform.scale(pg.image.load('images/canvas.png'), (48,48)) 

# coloca texto na tela
def texto(msg, cor, x, y, tam):
    font = pg.font.Font(None, tam)
    texto1 = font.render(msg, True, cor)
    win.blit(texto1, (x, y))

enemy_time = 1000 

# roda o jogo
def main():
    global pontuacao_anterior
    global enemy_time

    # estado de jogo
    game_state = 'start'

    # ticks do ultimo frame para calcular dt e fps
    ticks_last_frame = 0
    # ticks do ultimo inimigo para poder spawnar os inimigos
    ticks_last_enemy = 0

    # mude para true para ver o fps
    show_fps = False
    if show_fps:
        font = pg.font.Font(None, 20)
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

        # começa uma fase
        if pg.key.get_pressed()[pg.K_SPACE] and game_state == 'start':
            ticks_last_enemy = pg.time.get_ticks()
            game_state = 'play'

        # Calcula delta time, usado pra fazer o movimento continuo
        t = pg.time.get_ticks()
        dt = (t - ticks_last_frame)
        ticks_last_frame = t

        # roda a parte da gameplay
        if game_state == 'play':
            # responsavel por spawnar os inimigos
            dt_enemy = t - ticks_last_enemy
            if dt_enemy > enemy_time  and king.active_item['clock'] == -1:
                zombies.append(ini.inimigo(32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT, mapa))
                ticks_last_enemy = t

            # update o jogador e as balas
            king.update(dt, mapa)

            # reseta tudo e troca de mapa se o jogador morrer
            if king.health <= 0:
                # salva a pontuação atual para mostrar na tela se inicio da poxima fase
                pontuacao_anterior = collected_itens
                # muda o game_state
                game_state = 'start'
                # reseta tudo
                reset_all()
                
            # checka por inimigos em todas as balas
            for bullet in king.bullets:
                killed = bullet.check_enemy(zombies)
                # check_enemy() retorna -1 se a bala não está tocando em nenhum inimigo, caso contrario, ela retorna o inimigo
                if killed != -1:
                    if enemy_time > 300:
                        enemy_time -= 5
                    # toca o som de morte do inimigo
                    enemy_death.play()
                    # remove o inimigo da lista de inimigos
                    zombies.pop(zombies.index(killed))
                    # gera um número aleatório que vai determinar o item
                    rand = round((random()*1000)%100)
                    # só nasce um item se o número aleatório estiver nesse intervalo
                    if 0 <= rand < 62:
                        # cria um novo item
                        items.append(it.item(killed.x, killed.y, win, rand, t))

            # updates todos itens
            for item in items:
                item.update(t)
                # checa por itens coletados e adiciona eles no dicionário
                col = item.player_colision(king)
                # player_colision retorna -1 se o item não está tocando no jogador
                if col != -1 and col != 'S_coin':
                    collected_itens[col] += 1
                # S_coins contam como 10 coins normais
                if col == 'S_coin':
                    collected_itens['coin'] += 10
                # bootas e café tem influênci mecânica até o jogador morrer
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
                # multi_shot, fast_shot e clock são consumiveis, se o jogador coleta um e não tem nada em mãos,
                # ele pode usar mais tarde, se ele já tiver um item, ele automaticamente usa o item que acabou de coletar
                elif col in ['multi_shot', 'fast_shot', 'clock', 'wheel'] and king.current_item == None:
                    king.current_item = col
                else:
                    # o item está ativo quando ele tem um valor diferente de -1, o valor dado para o item
                    # representa o tempo no momento em que o item foi usado, esse tempo é usado para calcular quando
                    # item deve desaparecer
                    king.active_item[col] = t

                # remove os itens que não existem mais
                if item.existes == False:
                    items.pop(items.index(item))

            # print(king.current_item, collected_itens)
            # update do inimigo
            for zombie in zombies:
                # quando a função update do zombie recebe -1, eles não se movem
                # se o item 'clock' está ativado, os inimigos não saem do lugar
                if king.active_item['clock'] != -1:
                    zombie.update(-1, -1, dt, mapa)
                else:
                    # caso contrario, os inimigos recebem a posição atual do jogador para poder se mover em sua direção
                    zombie.update(king.x, king.y, dt, mapa)

            # desativa o item 'clock' se ele já está ativo a tempo suficiente
            if t-king.active_item['clock'] > king.item_duration/2:
                king.active_item['clock'] = -1

            # checa se algum inimigo está tocando o jogador e toca o som de dano
            if king.check_enemy(zombies, t):
                damage_sound.play()
            
            # isso é usa solução temporária para mostrar o item atual e a vida do jogador
            # o plano é mover isso para a tela do jogo

        # desenha tudo 
        draw_all(game_state)

        # mostra o fps do jogo e o dicionário de itens coletados
        if show_fps:
            fps = font.render(str(int(clock.get_fps())), True, pg.Color('Black'))
            win.blit(fps, (50, 50))
            itens = font.render(str(collected_itens), True, pg.Color('Black'))
            win.blit(itens, (50, 70))
            pg.display.flip()
            clock.tick(60)

        # update diplay
        pg.display.update()

itens_img = {'coin': pg.transform.scale(pg.image.load('images/coin.png'), (18,18)),
            'S_coin': pg.transform.scale(pg.image.load('images/coin_special.png'), (18,18)),
            'boots': pg.transform.scale(pg.image.load('images/boots.png'), (26,26)),
            'coffee': pg.transform.scale(pg.image.load('images/coffee.png'), (24,24)),
            'multi_shot': pg.transform.scale(pg.image.load('images/multi_shot.png'), (32,32)),
            'fast_shot': pg.transform.scale(pg.image.load('images/fast_shot.png'), (32,32)),
            'clock': pg.transform.scale(pg.image.load('images/clock.png'), (32,32))}

# vamos usar i para passar de mapa por mapa
i = 1

#  desenha tudo
def draw_all(game_state):
    # desenha o mapa
    mapa.draw()

    # desenhar inimigos
    for zombie in zombies:
        zombie.draw()

    # desenha os itens
    for item in items:
        item.draw()

    # desenha o jogador e as suas balas 
    king.draw()

    # desenha os corações do jogador
    for j in range(king.max_health):
        if j < king.health:
            win.blit(heart_full, ((40*j)+5,5))
        else:
            win.blit(heart_empty, ((40*j)+5,5))

    # desenha a caixa onde o item atual aparece
    win.blit(canvas, (620,5))

    # desenha o item atual acima da caixa
    if(king.current_item != None):
        win.blit(itens_img[king.current_item], (628, 13))

    global i
    if i == 1:
        color = (234, 222, 233)
    elif i == 2:
        color = (88, 29, 43)
    elif i == 3:
        color = (242, 188, 82)

    # desenho os itens coletaveis
    win.blit(itens_img['coin'], (8, 40))
    texto(f"x{collected_itens['coin']}", color, 30, 40, 30)
    win.blit(itens_img['coffee'], (7, 65))
    texto(f"x{collected_itens['coffee']}", color, 30, 69, 30)
    win.blit(itens_img['boots'], (5, 100))
    texto(f"x{collected_itens['boots']}", color, 30, 104, 30)

    # se o game_state está em start, mostre a pontuação das ultima/s fases junto da mensagem "press start"
    if game_state == 'start':
        if i == 1:
            texto(f"Pontuação total: {sum(pontuacao_total)}", (188, 51, 74), 220, 245, 35)
        else:
            texto(f"Pontuação anterior: {pontuacao_anterior['coin']}", (188, 51, 74), 220, 245, 35)
        win.blit(press_start, (200, 200))

    # faz update da tela
    pg.display.update()

# reseta o jogo
def reset_all():
    global pontuacao_total
    global i
    global collected_itens
    global enemy_time 
    enemy_time = 1000
    # quando i == 1, resetamos a pontuação total
    if i == 1:
        pontuacao_total = []
    # colocamos a quandidade de moedas dessa ultima partida na pontuação todal    
    pontuacao_total.append(collected_itens['coin'])
    # se i == 3, volte i para 1, voltando para o primeiro mapa
    if i == 3:
        i = 1
    # caso contrario, passa para o próximo mapa    
    else:
        i += 1

    global king 
    # recria o jogador 
    king =  pl.player((WINDOW_WIDTH // 2)-16, (WINDOW_HEIGHT // 2)-16, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)

    global zombies
    # recria a lista de inimigos como uma lista vazia, removendo todos inimigos
    zombies = []
    
    global items 
    # recria a lista de itens como uma lista vazia, removendo todos itens do mapa
    items = []
    
    global mapa
    # substitui o mapa atual pelo mapa sequinte 
    mapa = mp.mapa(0, 0, win, 'mapa'+str(i))

    # limpa o dicionario de itens coletados
    collected_itens = {'coin': 0,
                        'boots': 0,
                        'coffee': 0,
                        'multi_shot': 0,
                        'fast_shot': 0,
                        'clock': 0}


main()