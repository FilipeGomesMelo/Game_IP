import pygame as pg
import player as pl

# initialize Pygame
pg.init()

# dimenções da janela
WINDOW_WIDTH = 544
WINDOW_HEIGHT = 544

# setup da tela
win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Wild Wild West")

# setup icone da tela
icon = pg.image.load('images/cowboy.png')
pg.display.set_icon(icon)

# cria o jogador no centro da tela
king = pl.player(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 32, 32, win, WINDOW_WIDTH, WINDOW_HEIGHT)

# runs the game
def main():
    global king
    ticks_last_frame = 0
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
        # update o jogador e as balas
        king.update(dt)
        # desenha tudo
        draw_all()
        # update diplay
        pg.display.update()

#  desenha o jogador
def draw_all():
    # preenche o fundo
    win.fill((242,188,82))

    # desenha o jogador e as suas balas 
    king.draw()

    # faz update da tela
    pg.display.update()


main()    