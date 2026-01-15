class Setting():
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(255,255,255)
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.alien_drop_speed =20  # 向下掉落速度（10像素/次，可调整）
        self.fleet_drop_speed =20  # 整队向下移动速度（和drop_speed一致即可）
        #self.bullets_allowed=3  限制子弹数量为3
        self.fleet_drop_speed=10
        # 波次计数器（记录当前是第几波）
        self.wave = 1
        # 每波增加的数量（可调整）
        self.wave_increment = 2  # 每波最小/最大数量各加2
        self.min_alien_count = 5  # 初始最小外星人数量
        self.max_alien_count = 10  # 初始最大外星人数量
        self.ship_limit=3
        self.speedup_scale=1.1
        self.score_scale = 5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1
        self.fleet_direction=1#指示方向
        self.bullet_width = 7
        self.alien_points = 5
    def increase_speed(self):
        """提高速度设置，加快游戏进程"""
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_points = int(self.alien_points + self.score_scale)
        self.bullet_width += 20
