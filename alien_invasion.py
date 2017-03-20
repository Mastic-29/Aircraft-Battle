#E:\python代码\alien_invasion
#python .\alien_invasion.py
import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screenwidth,ai_settings.screenheight))
	pygame.display.set_caption("Alien Invasion")

	ship = Ship(screen,ai_settings)
	bullets = Group()
	aliens = Group()
	stats = GameStats(ai_settings)
	gf.create_fleet(ai_settings,screen,aliens,ship)
	play_button = Button(ai_settings,screen,"Play")
	sb = Scoreboard(ai_settings,stats,screen)
	while True:
		gf.check_events(ship,bullets,screen,ai_settings,stats,play_button,aliens,sb)#检查响应事件
		if stats.game_active:
			ship.update()#更新飞船位置
			gf.update_bullets(bullets,aliens,ai_settings,screen,ship,sb,stats)#更新子弹
			gf.update_aliens(aliens,ai_settings,ship,screen,stats,bullets,sb)#更新敌人
		gf.update_screen(ai_settings,ship,screen,bullets,aliens,play_button,stats,sb)#更新屏幕 ai_settings,ship,screen

run_game()