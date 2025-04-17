class GameStats:
    '''跟踪游戏的统计信息'''

    def __init__(self,ai_game):
        '''初始化统计信息'''
        self.settings=ai_game.settings
        self.reset_stats()  #运行了才会获得初始属性，不然在别的类中无法直接调用该方法中的属性

        #在任何情况下都不应该重置最高分，因此放在_init_()函数中定义
        self.high_score=0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left=self.settings.ship_limit  #重新将飞船剩余数量改回默认值
        self.score=0  #每次初始化时得分归零，把属性放在方法中定义，在别的类中想要重置属性时可以随时调用该方法
        self.level=1