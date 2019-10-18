#-*- coding:utf-8 -*-
__author__ = 'wzy'
import random
import pygame
# 屏幕大小的常量-一般设置跟北京图片一样的大小像素
SCREEN_RECT = pygame.Rect(0,0,480,700)
# 刷新的帧率，帧率越高，循环执行的次数越多
FRAME_PER_SEC = 90
# 创建敌机的定时器常量
# pygame.USEREVENT这个方法是创建一个用户事件，返回的是一个整数，所以可以在这个方法继续+1来创建其他用户事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄开发的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# 创建另外一台敌机
CREATE_ENEMY2_EVENT = pygame.USEREVENT + 2
# 创建大敌机
# CREATE_ENEMY3_EVENT = pygame.USEREVENT + 3

class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self,image_name,speed=1):

        # 调用父类的初始化方法
        super().__init__()

        #定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        #在屏幕的垂直方向下移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        #调用父类的方法实现
        super().update()

        # 2。 判断是否移除屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        # 1调用父类方法，创建敌机精灵，并同时指定敌机图片
        super().__init__("./images/enemy1.png")
        # 2指定敌机的初始随机速度
        self.speed = random.randint(1,4)

        # 3指定敌机的初始随机位置
        self.rect.bottom = 0

        # max_x就是获取敌机可以在右边的最大值，因为要减去敌机的宽度，才算是敌机可以到达右边的最大值
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)


    def update(self):

        # 调用父类方法，保持垂直方向的飞行
        super().update()
        # 判断是否飞出屏幕，如果是，就需要从精灵组中删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出了屏幕，需要从精灵组删除...")
            self.kill()

    # def __del__(self):
    #     print("敌机挂了(%s)" % self.rect)


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):

        super().__init__("./images/me1.png",0)
        #设置初始位置
        self.goto = None
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 60

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):

        #飞机水平移动
        if self.goto == 1:
            self.rect.x += self.speed
        elif self.goto == 2:
        #飞机垂直移动
            self.rect.y += self.speed

        #判断屏幕边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        if self.rect.bottom > SCREEN_RECT.height:
            self.rect.bottom = SCREEN_RECT.height
        if self.rect.y < (SCREEN_RECT.height)/2:
            self.rect.y = (SCREEN_RECT.height)/2



    def fire(self):
        # print("发射子弹...")
        for i in (0,1):
            # 1. 创建子弹精灵
            bullet = Bullet()
            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):

        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png",-2)
    def update(self):

        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom <0:
            self.kill()

        def __del__(self):
            print("子弹杯销毁")