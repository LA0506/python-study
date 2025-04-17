import pygame.font  #该模块可以把文本渲染到屏幕上

class Button:
    '''为游戏创建按钮的类'''

    def __init__(self,ai_game,msg):  #msg即我们想要在按钮中显示的文本
        '''初始化按钮的属性'''
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width,self.height=200,50
        self.button_color=(0,135,0)  #设置按钮颜色
        self.text_color=(255,255,255)  #设置文本颜色（白色）
        self.font=pygame.font.SysFont(None,48)  #设置字体与字号，默认字体，48号字号

        #创建按钮的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.height)  #创建一个矩形对象，坐标（0,0），尺寸是刚才设定的
        self.rect.center=self.screen_rect.center  #将该对象的center属性设置为屏幕的center属性

        #按钮的标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        '''将msg渲染为图像，并使其在按钮上居中'''
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)  #.font.render()将文本转换为图像，开启反锯齿，传入设定好的文本颜色和背景色
        self.msg_image_rect=self.msg_image.get_rect() #获得图像的矩形属性
        self.msg_image_rect.center=self.rect.center #将图像的center属性设定为按钮的center属性（即屏幕的center属性）

    def draw_button(self):
        '''绘制一个用颜色填充的按钮，再绘制文本'''
        self.screen.fill(self.button_color,self.rect)  #使用scree.fill()来对矩形进行颜色填充，绘制矩形
        self.screen.blit(self.msg_image,self.msg_image_rect)  #blit()对文本进行渲染，绘制文本图像