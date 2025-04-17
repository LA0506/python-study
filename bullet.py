import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''管理飞船所发射子弹的类'''

    def __init__(self,ai_game):
        '''在飞船的当前位置创建一个子弹对象'''
        super().__init__()  #继承从模块pygame.sprite中导入的Spirte类,通过使用该类可以对游戏中的某元素进行编组，进而同时操作编组中的所有元素

        self.screen=ai_game.screen  #引用实例中的屏幕
        self.settings=ai_game.settings  #引入设置
        self.color=self.settings.bullet_color  #传入提前设置好的子弹属性（颜色）


        #在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)  #在（0,0)处创建矩形，传入尺寸
        self.rect.midtop=ai_game.ship.rect.midtop  #子弹的矩形顶端对其飞船的顶端（即子弹的发射处）

        #存储用浮点表示子弹位置
        self.y=float(self.rect.y)  #设置子弹的y坐标存储为浮点数

    def update(self):
        '''向上移动子弹'''
        #更新子弹的准确位置
        self.y-=self.settings.bullet_speed  #不加限制的坐标变动，即自动移动
        #更新子弹的rect位置
        self.rect.y=self.y

    def draw_bullet(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen,self.color,self.rect)  #第一个参数指定在哪绘制，第二个绘制的颜色，第三个指定矩形属性
