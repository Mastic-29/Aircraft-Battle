import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullet(bullets,ai_settings,screen,ship):
	if len(bullets) < ai_settings.bullet_allowd:
		new_bullet = Bullet(screen,ship,ai_settings)#screen,ship,ai_settings
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_keydown_events(event,ship,bullets,screen,ai_settings):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(bullets,ai_settings,screen,ship)
	elif event.key == pygame.K_q:
		sys.exit()

def check_events(ship,bullets,screen,ai_settings,stats,play_button,aliens,sb):
	"""响应鼠标和键盘事件"""
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event,ship,bullets,screen,ai_settings)
			elif event.type == pygame.KEYUP:
				check_keyup_events(event,ship)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x,mouse_y = pygame.mouse.get_pos()
				check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship,sb):
	button_click = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_click and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,aliens,ship)#ai_settings,screen,aliens,ship
		ship.center_ship()

def update_screen(ai_settings,ship,screen,bullets,aliens,play_button,stats,sb):
	"""更新屏幕"""
	screen.fill(ai_settings.color)#画颜色
	ship.blitme()#画飞船

	for bullet in bullets.sprites():#画子弹
		bullet.draw_bullet()
	aliens.draw(screen)#画敌人
	sb.show_score()#画记分版
	
	if not stats.game_active:
		play_button.draw_button()
		
	pygame.display.flip()#显示

def check_bullets_aliens_collisions(bullets,aliens,ai_settings,screen,ship,sb,stats):
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)#检测子弹与敌人碰撞 并删除
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.aliens_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)

	if len(aliens) == 0:
		bullets.empty()
		create_fleet(ai_settings,screen,aliens,ship)#ai_settings,screen,aliens,ship
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()

def update_bullets(bullets,aliens,ai_settings,screen,ship,sb,stats):
	bullets.update()#更新子弹位置

	#删除消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullets_aliens_collisions(bullets,aliens,ai_settings,screen,ship,sb,stats)#检测子弹与敌人碰撞

def craete_alien(aliens,alien_number,screen,ai_settings,alien_number_row):
	alien = Alien(screen,ai_settings)#screen,ai_settings
	alien_width = alien.rect.width
	alien.x = alien_width+alien_number*2*(alien_width)
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height+alien_number_row*2*(alien.rect.height)
	aliens.add(alien)

def get_number_aliens_x(ai_settings,alien_width):
	available_space_x = ai_settings.screenwidth-(alien_width*2)
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
	available_space_y = ai_settings.screenheight-ship_height-3*(alien_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows

def create_fleet(ai_settings,screen,aliens,ship):
	'''创建外星人群'''
	alien = Alien(screen,ai_settings)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

	for alien_number_row in range(number_rows):
		for alien_number in range(number_aliens_x):
			craete_alien(aliens,alien_number,screen,ai_settings,alien_number_row)

def change_fleet_edges(aliens,ai_settings):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(aliens,ai_settings)
			break

def change_fleet_direction(aliens,ai_settings):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.alien_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,screen,aliens,ship,stats,bullets,sb):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings,screen,aliens,ship)
		ship.center_ship()
		sleep(0.5)
		sb.prep_ships()
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def update_aliens(aliens,ai_settings,ship,screen,stats,bullets,sb):
	change_fleet_edges(aliens,ai_settings)
	aliens.update()

	#检测飞船与敌人的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,aliens,ship,stats,bullets,sb)

	check_aliens_bottom(aliens,ai_settings,ship,screen,stats,bullets,sb)#检测敌人到达底部

def check_aliens_bottom(aliens,ai_settings,ship,screen,stats,bullets,sb):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,screen,aliens,ship,stats,bullets,sb)
			break

def check_high_score(stats,sb):
		if stats.high_score < stats.score:
			stats.high_score = stats.score
			sb.prep_high_score()