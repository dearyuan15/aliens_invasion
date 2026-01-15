# ship.py 正确代码（替换原文件内容）
import pygame as pg
import math
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船 + 倾斜摇晃参数"""
        super().__init__()  # 必须调用 Sprite 父类初始化
        self.screen = screen
        self.ai_settings = ai_settings

        # 1. 加载飞船图片（带异常处理，避免图片缺失崩溃）
        try:
            # 图片路径确保正确（根据你的项目结构调整）
            self.image_original = pg.image.load('images/ship.bmp')
        except Exception as e:
            print(f"飞船图片加载失败：{e}")
            # 兜底：创建红色矩形（确保能看到飞船）
            self.image_original = pg.Surface((80, 80))
            self.image_original.fill((255, 0, 0))  # 红色

        # 调整飞船尺寸（按需修改）
        self.image_original = pg.transform.scale(self.image_original, (80, 80))
        # 关键：给 Sprite 类指定 image 属性（必须！）
        self.image = self.image_original  # 初始为原图（未旋转偏移）
        # 关键：给 Sprite 类指定 rect 属性（必须！）
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 初始位置：屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 存储精确坐标（浮点数，用于平滑移动）
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # 移动标志（上下左右）
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 倾斜摇晃配置（可微调）
        self.shake_amplitude = 3  # 左右偏移幅度（3~5像素）
        self.tilt_angle_max = 3  # 最大倾斜角度（±3°，避免夸张）
        self.shake_frequency = 0.05  # 摇晃频率（0.05~0.1）
        self.shake_timer = 0  # 计时器

    def update(self):
        """更新飞船位置 + 摇晃计时器"""
        # 左右移动（带边界限制，避免超出屏幕）
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        # 上下移动（带边界限制）
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        # 同步精确坐标到 rect（rect 只接受整数）
        self.rect.centerx = int(self.centerx)
        self.rect.centery = int(self.centery)

        # 摇晃计时器累加（控制循环节奏）
        self.shake_timer += 1

    def center_ship(self):
        """飞船居中（修复原代码属性错误）"""
        self.centerx = self.screen_rect.centerx  # 用 centerx 而非 center
        self.centery = self.screen_rect.centery - 100  # 可调整垂直位置

    def blitme(self):
        """绘制飞船（含移动时的倾斜摇晃效果）"""
        is_moving = any([self.moving_right, self.moving_left, self.moving_up, self.moving_down])
        if is_moving:
            # 正弦函数生成平滑的偏移和倾斜角度
            sin_value = math.sin(self.shake_timer * self.shake_frequency)
            shake_x = self.shake_amplitude * sin_value  # 左右偏移
            tilt_angle = self.tilt_angle_max * sin_value  # 倾斜角度

            # 旋转图片（保持原尺寸）
            self.image_rotated = pg.transform.rotozoom(self.image_original, tilt_angle, 1.0)
            self.rect_rotated = self.image_rotated.get_rect()
            self.rect_rotated.center = self.rect.center  # 旋转后保持中心位置

            # 应用偏移并绘制
            draw_rect = self.rect_rotated.copy()
            draw_rect.x += int(shake_x)
            self.screen.blit(self.image_rotated, draw_rect)
        else:
            # 静止时绘制原图
            self.screen.blit(self.image_original, self.rect)