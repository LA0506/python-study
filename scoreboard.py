import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    '''显示得分信息的类'''

    def __init__(self,ai_game):
        '''初始化显示得分涉及的属性'''
        self.ai_game=ai_game  #将实例传递给属性,为了后面创建飞船实例，Ship（）中需要传入实例（主例）

        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats

        #显示得分信息时使用的字体设置
        self.text_color=(30,30,30)  #设置文本颜色
        self.font=pygame.font.SysFont(None,48)  #设置字体与字号

        #准备包含最高分和当前得分的图像，飞船的等级，剩余的飞船
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()




    def prep_score(self):
        '''将得分渲染为图像'''
        round_score=round(self.stats.score,-1)
        # score_str=str(self.stats.score)  #将数字转化为文本
        score_str=f"{round_score:,}"  #：，为格式说明符，会自动为前面数值加上逗号
        self.score_image=self.font.render(score_str,True,
                                          self.text_color,self.settings.bg_color)  #文本渲染

        #在屏幕右上角显示得分
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20  #在右上角显示（设置坐标）
        self.score_rect.top=20  #设置顶端距离20

    def prep_high_score(self):
        '''将最高分渲染为图像'''
        high_score=round(self.stats.high_score,-1)
        high_score_str=f"{high_score:,}"
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)

        #将最高分放在屏幕顶端的中央
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx  #放到屏幕的水平中央
        self.high_score_rect.top=self.score_rect.top  #和得分的纵坐标一样（同一水平高度）

    def prep_level(self):
        '''将等级渲染为图像'''
        level_str=str(self.stats.level)
        self.level_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        #将等级放在得分下面
        self.level_image_rect=self.level_image.get_rect()
        self.level_image_rect.right=self.score_rect.right
        self.level_image_rect.top=self.score_rect.bottom+10 #在得分下十个像素点绘制

    def prep_ships(self):
        '''显示还余下多少艘飞船'''
        self.ships=Group()  #创建编组
        for ship_number in range(self.stats.ships_left):  #根据还剩的飞船数量
            ship=Ship(self.ai_game)  #向Ship中传入实例（主例）
            ship.rect.x=10+ship_number*ship.rect.width  #在屏幕左上角10像素点位置，每个飞船间隔10像素点
            ship.rect.y=10  #左上角离屏幕上端10像素点
            self.ships.add(ship)  #循环加入编组

    def show_score(self):
        '''在屏幕显示得分，最高分和余下的飞船'''
        self.screen.blit(self.score_image,self.score_rect)  #因为只创建了文本转图像，因此没有创建矩形，填充矩形
        self.screen.blit(self.high_score_image,self.high_score_rect)  #绘制出最高得分
        self.screen.blit(self.level_image,self.level_image_rect)  #绘制出飞船等级
        self.ships.draw(self.screen)  #对编组调用draw()封装的blit，绘制到屏幕上
        
    def check_high_scores(self):
        '''检查是否出现了新的最高分'''
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()  #更新最高得分图像





