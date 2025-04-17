import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''

    def __init__(self,ai_game):
        '''初始化外星人并设置其起始位置'''
        super().__init__()
        self.screen=ai_game.screen

        #加载外星人图像并设置其rect属性
        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()

        #每个外星人最初都在屏幕的左上角附近
        self.rect.x=self.rect.width  #设置图像的坐标，左边距为外星人的宽度（图像的左上角是其（x,y）)
        self.rect.y=self.rect.height #设置上边距为外星人的高度  这样设置外星人出现在窗口左上角且较为美观

        #存储外星人的精确水平位置
        self.x=float(self.rect.x)  #比较关注外星人的水平移动速度，因此水平位置设定的更加精确些

        # 传入设置
        self.settings=ai_game.settings

    def check_edges(self):
        '''检测是否位于屏幕边缘'''
        screen_rect=self.screen.get_rect()
        return (self.rect.right>=screen_rect.right) or (self.rect.left<=0)  #检测是否到达屏幕边缘

    def update(self):
        '''向右移动外星人'''
        self.x+=self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x=self.x




