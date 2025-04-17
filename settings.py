class Settings:
    '''存储游戏《外星人入侵》中所有设置的类'''

    def __init__(self):
        '''初始化游戏的静态设置'''
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        #飞船设置
        self.ship_limit=3
        #子弹设置
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed=5  #限制子弹数量为5颗
        #外星人设置
        self.fleet_drop_speed=10  #碰到边缘后的向下移动速度
        #以什么速度加快游戏的节奏
        self.speedup_scale=1.1
        #外星人分数的提高速度（难度增加，击败得分也要增加）
        self.score_scale=1.5
        #记分设置
        self.alien_points=50

        self.initialize_dynamic_settings()  #在别的类中创建本类时会自动执行该函数，本函数是初始化游戏属性

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed=1.5
        self.bullet_speed=2.5
        self.alien_speed=1.0
        self.fleet_direction=1  #控制外星舰队水平移动方向的设置，1为向右

    def increase_speed(self):
        '''提高速度设置的值和外星人分数'''
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)  #保证外星人分数为整数
        print(self.alien_points)  #在终端窗口显示当前每个外星人的分数

