import pygame
from pygame.sprite import Sprite


class Ship(Sprite):  #引入精灵，为了后面方便一次性操作编组
    '''管理飞船的类'''

    def __init__(self, ai_game):  # ai_game后续会将AlienInvasion的实例引入其中，方便该类调用AlienInvasion中的游戏资源
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen = ai_game.screen  # 方便在该类中访问到屏幕（AlienIvnvasion实例）
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()  # 该函数能访问屏幕的rect（矩阵）属性，帮助我们能将飞船放到屏幕正确的位置

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')  # 获得图像，该函数返回表示一个飞船的surface,然后将这个surface赋给属性
        self.rect = self.image.get_rect()  # 获取该surface的属性rect，以便将来使用它来指定飞船的位置

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom  # 定义将飞船的矩形底部中点等于屏幕矩形的底部中点，即定位飞船位置

        # 在飞船的属性x中存储一个浮点数
        self.x = float(self.rect.x)  # 将飞船的矩形的x坐标转化为浮点型赋值给self.x，因为self.rect.x只能储存整数值，但速度可以设定为浮点值

        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船的位置'''
        if self.moving_right and self.rect.right<self.screen_rect.right:  # 如果向右移动标志为True时，向右移动一格 #更新：只有当同时飞船的矩形的右边缘坐标小于屏幕的右边缘坐标时才会接着更新self.x
            # self.rect.x+=1
            self.x += self.settings.ship_speed  # 引用settings中的速度设定来作为每次循环的移动距离
        if self.moving_left and self.rect.left>0:  # 反之，不使用elif，原因是存在elif时会优先判断if，那么当玩家同时按住左键和右键时，会向右移动，使用if则同时按下时不会移动  #更新：因为左边缘坐标就是0，因此只要大于0就还能接着向左移动
            self.x -= self.settings.ship_speed

        self.rect.x = self.x  # 再重新将self.x赋值给self.rect.x（只是为了后面绘制飞船时确定飞船的矩形属性）

    def center_ship(self):
        '''将飞船放在屏幕底部中央（飞船撞毁后重置飞船位置）'''
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)


    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)  # 根据图像self.image和飞船的矩形位置self.rect来绘制图像

# rect属性指该surface的位置坐标＋尺寸，get_rect(）就是获得该图形的rect属性，以便后续进行位置确定
