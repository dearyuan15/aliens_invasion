import sys
import pygame as pg
from bullet import Bullet
from alien import Alien
from time import sleep
import random
def check_keydown_events(event,ai_settings,screen,ship,bullets):
        if event.key==pg.K_RIGHT:
            ship.moving_right=True
        elif event.key==pg.K_LEFT:
            ship.moving_left=True
        elif event.key==pg.K_UP:
            ship.moving_up=True
        elif event.key==pg.K_DOWN:
            ship.moving_down=True
        elif event.key==pg.K_SPACE:
            #判断是否超过最大子弹数量
            #if len(bullets)<ai_settings.bullets_allowed:
            fire_bullet(ai_settings,screen,ship,bullets)
def fire_bullet(ai_settings,screen,ship,bullets):
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)
def check_keyup_events(event,ship):
    """响应鼠标和按键"""
    if event.key==pg.K_RIGHT:
        ship.moving_right = False
    elif event.key==pg.K_LEFT:
        ship.moving_left = False
    elif event.key==pg.K_UP:
        ship.moving_up=False
    elif event.key==pg.K_DOWN:
        ship.moving_down=False
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在点击play时开始游戏"""
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pg.mouse.set_visible(False)
        '''重置游戏统计信息'''
        stats.reset_stats()
        stats.game_active=True
        #重置计分的图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        """清空外星人和子弹"""
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type==pg.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pg.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_q:
                sys.exit()
            else:
                check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pg.KEYUP:
            check_keyup_events(event,ship)
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    '''更新屏幕，添加上外星人和子弹等一系列事物'''
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # 如果游戏处于非活动状态就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    pg.display.flip()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """更新子弹位置，删除超出屏幕的子弹"""
    bullets.update()
    # 删除超出屏幕顶部的子弹（避免内存泄漏）
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions=pg.sprite.groupcollide(bullets,aliens,False,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens)==0:
        #如果消灭了一波外星人，那么就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level+=1
        sb.prep_level()
        ai_settings.wave += 1
        create_fleet(ai_settings,screen,ship,aliens)
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
'''def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien=Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)'''
def create_random_alien(ai_settings, screen,ship, aliens):
    """创建一个随机位置的外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    screen_rect = screen.get_rect()
    ship_collision_rect = ship.rect.inflate(50, 50)  # 扩大50像素的飞船对应矩形，增大判定范围
    # 随机x坐标（确保不超出屏幕左右边缘）
    while True:
        max_x = screen_rect.width - alien_width  # 最大x值（右边缘）
        alien.x = random.uniform(alien_width, max_x)  # 随机x（避免贴边）
        alien.rect.x = alien.x

        # 随机y坐标（限制在屏幕上方1/2区域，避免初始位置过低）
        max_y = screen_rect.height // 2 - alien_height  # 最大y值（屏幕中间）
        alien.y = random.uniform(0, max_y)  # 随机y（从顶部开始）
        alien.rect.y = alien.y
        if not alien.rect.colliderect(ship_collision_rect):
            break  # 不重叠则退出循环
    aliens.add(alien)#alien.rect.colliderect(ship_collision_rect)用来判断两个矩形是否重叠，返回一个布尔值
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    # 创建一个外星人并计算每行可容纳多少个外星人
    '''alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)
'''
    """随机生成一组外星人（数量可自定义）"""
    # 随机生成5-10个外星人（可调整范围）
    """根据当前波次，随机生成递增数量的外星人"""
    # 计算当前波次的外星人数量范围（随波次增加）
    current_min = ai_settings.min_alien_count + (ai_settings.wave - 1) * ai_settings.wave_increment
    current_max = ai_settings.max_alien_count + (ai_settings.wave - 1) * ai_settings.wave_increment
    # 随机生成当前波次的外星人数量
    num_aliens = random.randint(current_min, current_max)

    # 随机位置生成外星人（复用之前的随机位置逻辑）
    for _ in range(num_aliens):
        # 调用随机生成单个外星人的函数（需补充此函数）
        create_random_alien(ai_settings, screen, ship,aliens)
def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移,并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
    if pg.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        print("You died!!")
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    #将ships_left -1
    if stats.ships_left>0:
        stats.ships_left-=1
        #更新计分牌
        sb.prep_ships()
        #清空外星人和子弹，相当于重开一次
        aliens.empty()
        bullets.empty()
        #清空后要添加一群新外星人并将飞船归位，对应重开一局
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #(暂停一下)
        sleep(0.5)
    else:
        ai_settings.wave=1
        stats.game_active=False
        pg.mouse.set_visible(True)
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        #对此处理类似飞船的碰撞
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """检查是否产生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()