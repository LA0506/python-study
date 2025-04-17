<<<<<<< HEAD
import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


# 1.设定窗口大小和背景色，设定游戏控制方法（循环），增加Settings类
# 2.添加飞船图像，增加Ship类
# 3.驾驶飞船（控制飞船移动，持续移动，改变移动速度，限制飞船的活动范围
# 4.创建外星人
# 5.创建一行外星人，创建多行外星人
# 6.让外星人移动（向右移动，碰到边缘，向下移动，后改变水平移动方向）
# 6.击落外星人
# 7.全歼外星人或飞船被摧毁
# 8.添加Play按钮,鼠标点击Play游戏开始，将Play切换到非活动状态，隐藏光标
# 9.提高难度，增加外星人得分
# 10.储存最高分
# 11.显示等级



class AlienInvasion:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()  # 调用该函数来初始化背景

        # self.screen = pygame.display.set_mode(
        #     (1200, 800))  # 创建一个显示窗口，这个游戏的所有图形元素都将在其中绘制（1200,800)表示宽1200像素，高800像素，讲这个显示窗口赋给属性self.screen，让这个类的所有方法都能够使用它
        #
        self.clock = pygame.time.Clock()  # 调用自带的类进行控制帧率
        #
        # #设置背景色
        # self.bg_color=(230,230,230)   #实质是个元组，存储颜色数据，红，绿，蓝每个的取值为0-255，设置每个为230，实际呈现出一种浅灰色
        self.settings = Settings()  # 上述窗口设置和背景色设置转到Settings类中设置了，可以在设置类中进行设置修改（类中设置属性），不用到处寻找设置进行修改

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )  # 创建窗口将窗口属性传递进去（从提前设定好的实例中的属性）

        # 创建全屏的窗口：
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion')  # 设置显示窗口抬头

        # 创建一个用于储存游戏统计信息的实例,并创建记分牌
        self.stats = GameStats(self)
        self.sb=Scoreboard(self)
        self.ship = Ship(self)  # 因为在Ship类中调用过该类，所以使用self指向AlienInvasion实例，以便Ship类能够调用该类的游戏资源
        self.bullets = pygame.sprite.Group()  # 创建子弹编组（现在还是个空编组）
        self.aliens = pygame.sprite.Group()  # 创建外星人编组

        self._create_fleet()  # 执行我定义的创建外星舰队的方法(最初始的创建外星舰队，但实际上只是创建了编组，绘制图象在别的方法里）
        #让游戏一开始处于非活动状态
        self.game_active=False  #点击Play之后才能游戏

        #创建Play按钮
        self.play_button=Button(self,'Play')  #传入msg文本


    def run_game(self):  # 这个游戏由该方法控制
        '''开始游戏的主循环'''
        while 1:
            # 对原方法进行重构，将不同的功能分离出去设立新的方法，以便后续维护和增添新的代码
            self._check_events()

            if self.game_active:  #除了获取事件与屏幕更新，其他的方法运行都要在游戏处于活动状态（飞船，子弹，外星人都有，但不会动，也不能操作）
                self.ship.update()  # 在循环中根据按下或松开向右按键来控制向右标志，进而控制在循环中的向右移动（即如果一直按着，就可以持续向右移动）
                self._update_bullets()
                self.update_aliens()

            self._update_screen()
            self.clock.tick(60)  # 在主循环中控制这个循环尽可能每秒运行60次

            # #侦听键盘和鼠标事件（玩家的每一次操作就是一次事件，编写一次事件循环）
            # for event in pygame.event.get():  #使用该函数来访问pygame检测到的事件，该函数会返回一个列表，包含它在上一次调用后发生的所有事件，所有键盘和鼠标事件都将导致这个for循环运行
            #     if event.type==pygame.QUIT:  #如果事件是pygame.QUIT事件，就调用sys.exit()来退出游戏
            #         sys.exit()

            # #每次循环时都重绘屏幕
            # self.screen.fill(self.settings.bg_color)  #对屏幕进行填充背景色，传入之前设置好的颜色数据(修改：传入实例中提前设定好的属性）
            # self.ship.blitme()  #绘制飞船
            #
            # #让最近绘制的屏幕可见（并更新元素位置）
            # pygame.display.flip()   #while循环的时候每次都会绘制一个空屏幕，并擦去旧屏幕，使得只有新的空屏幕可见，使用该函数将不断更新屏幕，以显示新位置上的元素并隐藏原来位置上的元素，从而营造平滑移动的效果

    def _check_events(self):  # 类内调用，一般加函数前_,是辅助方法
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 检查是否触发按键按下事件（按下一次会记录一次事件）
                self._check_events_keydown(event)
                # if event.key==pygame.K_RIGHT:  #检查按下的键是否为向右按键
                #     # self.ship.rect.x+=1  #   #飞船的矩形的x坐标＋1（向右移动1格）,不使用这种移动方式（因为不能持续移动）
                #     self.ship.moving_right=True
                # elif event.key==pygame.K_LEFT:  #这里之所以可以使用elif（而不是if）原因是每次进行按键操作都会被记录为事件，参与一次for提取然后进行判断，因此elif与if有同样的实际优先级
                #     self.ship.moving_left=True
            elif event.type == pygame.KEYUP:  # 按键松开事件
                self._check_events_keyup(event)
                # if event.key==pygame.K_RIGHT:
                #     self.ship.moving_right=False
                # elif event.key==pygame.K_LEFT:
                #     self.ship.moving_left=False

            elif event.type==pygame.MOUSEBUTTONDOWN:  #鼠标点击事件
                mouse_pos=pygame.mouse.get_pos()  #获得鼠标点击的(x,y)
                self._check_play_button(mouse_pos)  #执行辅助方法


    def _check_events_keydown(self, event):
        '''按键按下事件'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # 新增按下按键Q时结束游戏
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 按动空格时调用方法

    def _check_events_keyup(self, event):
        '''按键松开事件'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self,mouse_pos):
        '''在玩家单点Play按钮时开始新游戏'''
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)  #检测鼠标点击的位置是否在play_button的rect内  #更新：赋值
        if button_clicked and not self.game_active:  #仅当玩家单点了Play且游戏未开始的情况下才会开始游戏
            #重置游戏的统计信息
            self.stats.reset_stats()  #GameStats类中提前设置好的方法  飞船数量变回默认值
            self.sb.prep_score()  #在新一局游戏开始之后，虽然分数已经在上面方法更新，但是没有将文本绘制为图像，因此_up_screen()方法中还是绘制的上一局分数
            self.sb.prep_level()  #重置等级后，更新等级图像
            self.sb.prep_ships()  #游戏开始更新剩余飞船数图像
            self.game_active=True  #重新开始游戏

            #还原游戏设置
            self.settings.initialize_dynamic_settings()  #重新开始游戏时需要还原游戏设置

            # 清空外星人列表和子弹列表（编组）
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星人舰队，并将飞船重新放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            #游戏开始后隐藏光标
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets'''
        if len(self.bullets) < self.settings.bullets_allowed:  # 当未消失的子弹数目（未删除）小于设置值时可创建子弹
            new_bullet = Bullet(self)  # 创建实例并赋值  也是在这里将Alien实例传入bullet类
            self.bullets.add(new_bullet)  # 将实例加入编组

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        # 更新子弹的位置
        self.bullets.update()  # 编组允许对整个编组里的所有精灵调用函数（而不像飞船只有一个，更新飞船的坐标即可）

        # 删除已消失的子弹
        for bullet in self.bullets.copy():  # 因为在for遍历时，不能改变列表的长度，因此我们可以使用copy（）创建可以遍历删除的副本
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collision()
        # #检查是否有子弹击中了外星人（在更新子弹位置之后，绘制子弹之前执行）
        # #如果是，就删除相应的子弹和外星人
        # collisions=pygame.sprite.groupcollide(
        #     self.bullets,self.aliens,True,True
        # )  #该方法检测两个编组内是否有元素rect重叠，当重叠时返回一个字典，后面两个True表示两个元素都删除（第一个对应子弹，第二个对应外星人）



    def _check_bullet_alien_collision(self):  # 重构
        '''检查是否有子弹击中了外星人（在更新子弹位置之后，绘制子弹之前执行）'''
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )  # 该方法检测两个编组内是否有元素rect重叠，当重叠时返回一个字典，后面两个True表示两个元素都删除（第一个对应子弹，第二个对应外星人）

        if collisions:  #如果字典中有元素（击毁外星人）
            self.stats.score+=self.settings.alien_points  #记分属性＋50
            self.sb.prep_score()  #更新图像
            self.sb.check_high_scores()  #检查是否出现新的最高得分（该方法中包含了更新最高得分图像）


        # 如果外星人舰队杀光了，刷新，并清空现有子弹
        if not self.aliens:  #如果外星舰队全消灭了
            self.bullets.empty()  # 清空编组
            self._create_fleet()  # 重新创建外星人舰队
            self.settings.increase_speed()  #当外星舰队全部被击落，提升玩家等级和游戏难度

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()  #更新等级图像


    def _create_fleet(self):
        '''创建一个外星舰队'''
        # 创建一个外星人，再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # 解包 同时得到得到图像宽度和图像高度  rect.size是个元组，包含宽度和高度

        current_x = alien_width  # 设置图像的x坐标
        current_y = alien_height  # 设置图像的y坐标
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):  # 间隔一个外星人宽度，加上自身宽度，因此至少留下两个外星人宽度
                # new_alien = Alien(self)  # 创建实例
                # new_alien.x = current_x  # 设置外星人的x精确坐标，可用于后续移动
                # new_alien.rect.x = current_x  # 同步外星人的rect.x坐标（整数坐标），用于实际绘图
                # self.aliens.add(new_alien)
                self._create_alien(current_x, current_y)  # 调用辅助方法，循环创建外星人（外星人舰队）直至占满整行  #创建多列
                current_x += 2 * alien_width  # 每个外星人间隔一个外星人宽度，加上自身宽度，因此每次外星人的x坐标水平移动两个外星人宽度

            # 添加一行后，需重置x坐标，并改变y坐标（从新的一行开始）
            current_x = alien_width
            current_y += 2 * alien_height  # 还是隔一个外星人高度创建新的一行

    def _create_alien(self, x_position, y_position):
        '''创建一个外星人，并将其加入外星舰队'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position  # 只要给图像加上y坐标即可（之前是使用的alien类中的默认y坐标，现在重新赋值）
        self.aliens.add(new_alien)

    def update_aliens(self):
        '''先检测是否到达边缘，是否采取措施，然后更新外星舰队中所有外星人的位置'''
        self._check_fleet_edges()  # 调用辅助方法检测并采取措施
        self.aliens.update()  # 不是简单的调用Alien类中的方法，而是对外星人编组使用该方法

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # 检测是否有元素与编组中的元素碰撞，检测到返回True
            self._ship_hit()  #如果碰到，执行该方法
        #检测是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        '''当外星舰队到达边缘时采取的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():  # 调用Alien类中方法，如果到达边缘
                self._change_fleet_direction()  # 采取措施
                break

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕的下边缘'''
        for alien in self.aliens.sprites():  #有一个外星人到达屏幕底部，就等同于飞船死了一次
            if alien.rect.bottom>=self.settings.screen_height:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break  #有一只外星人撞到就不用再检查其他外星人了


    def _ship_hit(self):
        '''响应飞船和外星人的碰撞'''
        if self.stats.ships_left>0:
            # 将ship_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()  #更新飞船数目

            # 清空外星人列表和子弹列表（编组）
            self.bullets.empty()
            self.aliens.empty()  #清空外星人的同时，创建外星人舰队，因此不会触发increase_speed（）函数

            # 创建一个新的外星人舰队，并将飞船重新放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active=False  #当剩余飞船数量小于等于0时游戏结束
            pygame.mouse.set_visible(True)  #游戏结束光标出现



    def _change_fleet_direction(self):
        '''将整个舰队向下移动，并改变左右移动方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # 所有外星人瞬间下移（y坐标改变）不是持续向下移动
        self.settings.fleet_direction *= -1  # 在下次到达屏幕边缘前一直改变左右移动方向

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():  # bullets.spirtes返回一个编组列表，遍历列表中的所有精灵
            bullet.draw_bullet()  # 对每个精灵调用该函数（绘制出子弹）    类似里面都是百变怪，每个百变怪可使用该方法绘制出来，不加screen原因同下，在原类中已经加过screen，这里之所以不像外星人一样group.draw(），是因为子弹是矩形，用draw.rect()绘制
        self.ship.blitme()  # 绘制飞船，不加screen是因为，这是调用Ship类中的方法，在该方法中已经screen.blit()过
        self.aliens.draw(self.screen)  # 绘制外星人，绘制到屏幕上

        #显示得分
        self.sb.show_score()

        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()  #只有在游戏未开始状态时才会绘制Play图标

        pygame.display.flip()

        '''
        draw_rect() 一般用于绘制矩形，纯色块（有边框）
        fill()对矩形进行颜色填充（无边框）
        blit()文本渲染，或者绘制图像/group.draw()实际是封装的blit()，对编组中的所有元素进行blit()
        存在文本转化为图像的话，需要先使用.font.render(msg,...)将文本转化为图像，然后再使用fill()和blit()绘制图形
        '''

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
=======
import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


# 1.设定窗口大小和背景色，设定游戏控制方法（循环），增加Settings类
# 2.添加飞船图像，增加Ship类
# 3.驾驶飞船（控制飞船移动，持续移动，改变移动速度，限制飞船的活动范围
# 4.创建外星人
# 5.创建一行外星人，创建多行外星人
# 6.让外星人移动（向右移动，碰到边缘，向下移动，后改变水平移动方向）
# 6.击落外星人
# 7.全歼外星人或飞船被摧毁
# 8.添加Play按钮,鼠标点击Play游戏开始，将Play切换到非活动状态，隐藏光标
# 9.提高难度，增加外星人得分
# 10.储存最高分
# 11.显示等级



class AlienInvasion:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()  # 调用该函数来初始化背景

        # self.screen = pygame.display.set_mode(
        #     (1200, 800))  # 创建一个显示窗口，这个游戏的所有图形元素都将在其中绘制（1200,800)表示宽1200像素，高800像素，讲这个显示窗口赋给属性self.screen，让这个类的所有方法都能够使用它
        #
        self.clock = pygame.time.Clock()  # 调用自带的类进行控制帧率
        #
        # #设置背景色
        # self.bg_color=(230,230,230)   #实质是个元组，存储颜色数据，红，绿，蓝每个的取值为0-255，设置每个为230，实际呈现出一种浅灰色
        self.settings = Settings()  # 上述窗口设置和背景色设置转到Settings类中设置了，可以在设置类中进行设置修改（类中设置属性），不用到处寻找设置进行修改

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )  # 创建窗口将窗口属性传递进去（从提前设定好的实例中的属性）

        # 创建全屏的窗口：
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion')  # 设置显示窗口抬头

        # 创建一个用于储存游戏统计信息的实例,并创建记分牌
        self.stats = GameStats(self)
        self.sb=Scoreboard(self)
        self.ship = Ship(self)  # 因为在Ship类中调用过该类，所以使用self指向AlienInvasion实例，以便Ship类能够调用该类的游戏资源
        self.bullets = pygame.sprite.Group()  # 创建子弹编组（现在还是个空编组）
        self.aliens = pygame.sprite.Group()  # 创建外星人编组

        self._create_fleet()  # 执行我定义的创建外星舰队的方法(最初始的创建外星舰队，但实际上只是创建了编组，绘制图象在别的方法里）
        #让游戏一开始处于非活动状态
        self.game_active=False  #点击Play之后才能游戏

        #创建Play按钮
        self.play_button=Button(self,'Play')  #传入msg文本


    def run_game(self):  # 这个游戏由该方法控制
        '''开始游戏的主循环'''
        while 1:
            # 对原方法进行重构，将不同的功能分离出去设立新的方法，以便后续维护和增添新的代码
            self._check_events()

            if self.game_active:  #除了获取事件与屏幕更新，其他的方法运行都要在游戏处于活动状态（飞船，子弹，外星人都有，但不会动，也不能操作）
                self.ship.update()  # 在循环中根据按下或松开向右按键来控制向右标志，进而控制在循环中的向右移动（即如果一直按着，就可以持续向右移动）
                self._update_bullets()
                self.update_aliens()

            self._update_screen()
            self.clock.tick(60)  # 在主循环中控制这个循环尽可能每秒运行60次

            # #侦听键盘和鼠标事件（玩家的每一次操作就是一次事件，编写一次事件循环）
            # for event in pygame.event.get():  #使用该函数来访问pygame检测到的事件，该函数会返回一个列表，包含它在上一次调用后发生的所有事件，所有键盘和鼠标事件都将导致这个for循环运行
            #     if event.type==pygame.QUIT:  #如果事件是pygame.QUIT事件，就调用sys.exit()来退出游戏
            #         sys.exit()

            # #每次循环时都重绘屏幕
            # self.screen.fill(self.settings.bg_color)  #对屏幕进行填充背景色，传入之前设置好的颜色数据(修改：传入实例中提前设定好的属性）
            # self.ship.blitme()  #绘制飞船
            #
            # #让最近绘制的屏幕可见（并更新元素位置）
            # pygame.display.flip()   #while循环的时候每次都会绘制一个空屏幕，并擦去旧屏幕，使得只有新的空屏幕可见，使用该函数将不断更新屏幕，以显示新位置上的元素并隐藏原来位置上的元素，从而营造平滑移动的效果

    def _check_events(self):  # 类内调用，一般加函数前_,是辅助方法
        '''响应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 检查是否触发按键按下事件（按下一次会记录一次事件）
                self._check_events_keydown(event)
                # if event.key==pygame.K_RIGHT:  #检查按下的键是否为向右按键
                #     # self.ship.rect.x+=1  #   #飞船的矩形的x坐标＋1（向右移动1格）,不使用这种移动方式（因为不能持续移动）
                #     self.ship.moving_right=True
                # elif event.key==pygame.K_LEFT:  #这里之所以可以使用elif（而不是if）原因是每次进行按键操作都会被记录为事件，参与一次for提取然后进行判断，因此elif与if有同样的实际优先级
                #     self.ship.moving_left=True
            elif event.type == pygame.KEYUP:  # 按键松开事件
                self._check_events_keyup(event)
                # if event.key==pygame.K_RIGHT:
                #     self.ship.moving_right=False
                # elif event.key==pygame.K_LEFT:
                #     self.ship.moving_left=False

            elif event.type==pygame.MOUSEBUTTONDOWN:  #鼠标点击事件
                mouse_pos=pygame.mouse.get_pos()  #获得鼠标点击的(x,y)
                self._check_play_button(mouse_pos)  #执行辅助方法


    def _check_events_keydown(self, event):
        '''按键按下事件'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # 新增按下按键Q时结束游戏
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 按动空格时调用方法

    def _check_events_keyup(self, event):
        '''按键松开事件'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self,mouse_pos):
        '''在玩家单点Play按钮时开始新游戏'''
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)  #检测鼠标点击的位置是否在play_button的rect内  #更新：赋值
        if button_clicked and not self.game_active:  #仅当玩家单点了Play且游戏未开始的情况下才会开始游戏
            #重置游戏的统计信息
            self.stats.reset_stats()  #GameStats类中提前设置好的方法  飞船数量变回默认值
            self.sb.prep_score()  #在新一局游戏开始之后，虽然分数已经在上面方法更新，但是没有将文本绘制为图像，因此_up_screen()方法中还是绘制的上一局分数
            self.sb.prep_level()  #重置等级后，更新等级图像
            self.sb.prep_ships()  #游戏开始更新剩余飞船数图像
            self.game_active=True  #重新开始游戏

            #还原游戏设置
            self.settings.initialize_dynamic_settings()  #重新开始游戏时需要还原游戏设置

            # 清空外星人列表和子弹列表（编组）
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星人舰队，并将飞船重新放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            #游戏开始后隐藏光标
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets'''
        if len(self.bullets) < self.settings.bullets_allowed:  # 当未消失的子弹数目（未删除）小于设置值时可创建子弹
            new_bullet = Bullet(self)  # 创建实例并赋值  也是在这里将Alien实例传入bullet类
            self.bullets.add(new_bullet)  # 将实例加入编组

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        # 更新子弹的位置
        self.bullets.update()  # 编组允许对整个编组里的所有精灵调用函数（而不像飞船只有一个，更新飞船的坐标即可）

        # 删除已消失的子弹
        for bullet in self.bullets.copy():  # 因为在for遍历时，不能改变列表的长度，因此我们可以使用copy（）创建可以遍历删除的副本
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collision()
        # #检查是否有子弹击中了外星人（在更新子弹位置之后，绘制子弹之前执行）
        # #如果是，就删除相应的子弹和外星人
        # collisions=pygame.sprite.groupcollide(
        #     self.bullets,self.aliens,True,True
        # )  #该方法检测两个编组内是否有元素rect重叠，当重叠时返回一个字典，后面两个True表示两个元素都删除（第一个对应子弹，第二个对应外星人）



    def _check_bullet_alien_collision(self):  # 重构
        '''检查是否有子弹击中了外星人（在更新子弹位置之后，绘制子弹之前执行）'''
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )  # 该方法检测两个编组内是否有元素rect重叠，当重叠时返回一个字典，后面两个True表示两个元素都删除（第一个对应子弹，第二个对应外星人）

        if collisions:  #如果字典中有元素（击毁外星人）
            self.stats.score+=self.settings.alien_points  #记分属性＋50
            self.sb.prep_score()  #更新图像
            self.sb.check_high_scores()  #检查是否出现新的最高得分（该方法中包含了更新最高得分图像）


        # 如果外星人舰队杀光了，刷新，并清空现有子弹
        if not self.aliens:  #如果外星舰队全消灭了
            self.bullets.empty()  # 清空编组
            self._create_fleet()  # 重新创建外星人舰队
            self.settings.increase_speed()  #当外星舰队全部被击落，提升玩家等级和游戏难度

            #提高等级
            self.stats.level+=1
            self.sb.prep_level()  #更新等级图像


    def _create_fleet(self):
        '''创建一个外星舰队'''
        # 创建一个外星人，再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size  # 解包 同时得到得到图像宽度和图像高度  rect.size是个元组，包含宽度和高度

        current_x = alien_width  # 设置图像的x坐标
        current_y = alien_height  # 设置图像的y坐标
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):  # 间隔一个外星人宽度，加上自身宽度，因此至少留下两个外星人宽度
                # new_alien = Alien(self)  # 创建实例
                # new_alien.x = current_x  # 设置外星人的x精确坐标，可用于后续移动
                # new_alien.rect.x = current_x  # 同步外星人的rect.x坐标（整数坐标），用于实际绘图
                # self.aliens.add(new_alien)
                self._create_alien(current_x, current_y)  # 调用辅助方法，循环创建外星人（外星人舰队）直至占满整行  #创建多列
                current_x += 2 * alien_width  # 每个外星人间隔一个外星人宽度，加上自身宽度，因此每次外星人的x坐标水平移动两个外星人宽度

            # 添加一行后，需重置x坐标，并改变y坐标（从新的一行开始）
            current_x = alien_width
            current_y += 2 * alien_height  # 还是隔一个外星人高度创建新的一行

    def _create_alien(self, x_position, y_position):
        '''创建一个外星人，并将其加入外星舰队'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position  # 只要给图像加上y坐标即可（之前是使用的alien类中的默认y坐标，现在重新赋值）
        self.aliens.add(new_alien)

    def update_aliens(self):
        '''先检测是否到达边缘，是否采取措施，然后更新外星舰队中所有外星人的位置'''
        self._check_fleet_edges()  # 调用辅助方法检测并采取措施
        self.aliens.update()  # 不是简单的调用Alien类中的方法，而是对外星人编组使用该方法

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # 检测是否有元素与编组中的元素碰撞，检测到返回True
            self._ship_hit()  #如果碰到，执行该方法
        #检测是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        '''当外星舰队到达边缘时采取的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():  # 调用Alien类中方法，如果到达边缘
                self._change_fleet_direction()  # 采取措施
                break

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕的下边缘'''
        for alien in self.aliens.sprites():  #有一个外星人到达屏幕底部，就等同于飞船死了一次
            if alien.rect.bottom>=self.settings.screen_height:
                #像飞船被撞到一样进行处理
                self._ship_hit()
                break  #有一只外星人撞到就不用再检查其他外星人了


    def _ship_hit(self):
        '''响应飞船和外星人的碰撞'''
        if self.stats.ships_left>0:
            # 将ship_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()  #更新飞船数目

            # 清空外星人列表和子弹列表（编组）
            self.bullets.empty()
            self.aliens.empty()  #清空外星人的同时，创建外星人舰队，因此不会触发increase_speed（）函数

            # 创建一个新的外星人舰队，并将飞船重新放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active=False  #当剩余飞船数量小于等于0时游戏结束
            pygame.mouse.set_visible(True)  #游戏结束光标出现



    def _change_fleet_direction(self):
        '''将整个舰队向下移动，并改变左右移动方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  # 所有外星人瞬间下移（y坐标改变）不是持续向下移动
        self.settings.fleet_direction *= -1  # 在下次到达屏幕边缘前一直改变左右移动方向

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():  # bullets.spirtes返回一个编组列表，遍历列表中的所有精灵
            bullet.draw_bullet()  # 对每个精灵调用该函数（绘制出子弹）    类似里面都是百变怪，每个百变怪可使用该方法绘制出来，不加screen原因同下，在原类中已经加过screen，这里之所以不像外星人一样group.draw(），是因为子弹是矩形，用draw.rect()绘制
        self.ship.blitme()  # 绘制飞船，不加screen是因为，这是调用Ship类中的方法，在该方法中已经screen.blit()过
        self.aliens.draw(self.screen)  # 绘制外星人，绘制到屏幕上

        #显示得分
        self.sb.show_score()

        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()  #只有在游戏未开始状态时才会绘制Play图标

        pygame.display.flip()

        '''
        draw_rect() 一般用于绘制矩形，纯色块（有边框）
        fill()对矩形进行颜色填充（无边框）
        blit()文本渲染，或者绘制图像/group.draw()实际是封装的blit()，对编组中的所有元素进行blit()
        存在文本转化为图像的话，需要先使用.font.render(msg,...)将文本转化为图像，然后再使用fill()和blit()绘制图形
        '''

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
>>>>>>> eb7f52a809a12086743c2d325a136a0079f26739
