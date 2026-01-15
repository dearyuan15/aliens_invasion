import sys
import pygame as pg
from setting import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
    pg.init()#初始化背景设置
    ai_settings=Setting()
    screen=pg.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pg.display.set_caption("三班内战")
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    #创建一个用于存储游戏信息的实例
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    ship=Ship(ai_settings,screen)
    #alien=Alien(ai_settings,screen)
    bullets=Group()
    aliens=Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
            #ship.blitme()
run_game()