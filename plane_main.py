#-*- coding:utf-8 -*-
__author__ = 'wzy'
import pygame
import time,sys
from plane_sprites import  *

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        # print("游戏初始化")

        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2。创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4.设定定时器事件，创建敌机 1s创建一个
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        # 5.设定子弹的定时器时间，每0.4s发射一颗子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, 400)
        # 6.设置定时器事件，创建敌机2 4s创建一个
        pygame.time.set_timer(CREATE_ENEMY2_EVENT, 4000)
        # pygame.time.set_timer(CREATE_ENEMY3_EVENT, 1000)
        # 7. 初始化记分牌，来获取玩家的得分情况
        self.count_die_enemy = 0
        self.hero_life = 3

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()
        # 英雄初始化
        self.hero =Hero()
        self.hero_group = pygame.sprite.Group(self.hero)



    def start_game(self):
        # print("游戏开始")
        while True:

            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 2. 事件监听
            self.__event_handler()

            # 3. 碰撞检测
            self.__check_collide()

            # 4. 更新精灵组
            self.__update_sprites()

            # 5. 更新屏幕显示
            pygame.display.update()



    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出场")
                # 创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到敌机精灵组里面去
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                #判断是否是英雄开火的事件，如果是，就开火
                self.hero.fire()
            elif event.type == CREATE_ENEMY2_EVENT:
                # print("敌机2出场")
                # 创建敌机精灵
                enemy2 = Enemy()
                #这里要更换敌机2的图片
                enemy2.image=pygame.image.load("./images/enemy2.png")
                self.enemy_group.add(enemy2)

        # 使用键盘提供的方法获取键盘按键 - 按键元组--》返回一个元组
        # 如果被按下了，就是那个键为1,否则就是0
        keys_pressed = pygame.key.get_pressed()
        # print("keys_pressed:",keys_pressed)
        # 判断元组中对应的按键索引值,像pygame.K_RIGHT可以打印这个键在元组中的位置，这里pygame.K_RIGHT是275的位置
        if keys_pressed[pygame.K_RIGHT]:
            #如果被按下了，那么对应元组的第275个的值就是1，就可以进来这里
            #设置移动速度为3
            self.hero.speed = 3
            #设置水平移动参数
            self.hero.goto = 1
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -3
            self.hero.goto = 1
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed = -3
            #设置垂直移动参数
            self.hero.goto = 2
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed = 3
            self.hero.goto = 2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 1.子弹摧毁敌机--参数都是精灵组
        cal_num=pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        # pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        if len(cal_num) > 0:
            self.count_die_enemy += 1
            if self.count_die_enemy > 30 and self.count_die_enemy <= 90:
                pygame.time.set_timer(CREATE_ENEMY_EVENT,500)
                pygame.time.set_timer(CREATE_ENEMY2_EVENT, 2000)
            elif self.count_die_enemy > 90 and self.count_die_enemy <= 150:
                pygame.time.set_timer(CREATE_ENEMY_EVENT,250)
                pygame.time.set_timer(CREATE_ENEMY2_EVENT, 1000)
            elif self.count_die_enemy > 150:
                print("游戏结束，你通关了")
                time.sleep(2)
                sys.exit()
        # 2.敌机撞毁英雄-这里会返回精灵组的一个列表-如果没有发生碰撞，列表为空列表
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(enemies) >0:
            self.hero_life -= 1
            if self.hero_life == 0:
                # print("The Game Over,Your Score is :【%s】" % self.count_die_enemy)
                time.sleep(1)
                self.hero.kill()
                #结束游戏
                try:
                    PlaneGame.__game_over()
                except TypeError as result:
                    print("英雄被撞毁，游戏结束，你的得分是【%s】" % self.count_die_enemy)
                    sys.exit()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)



    @staticmethod
    def __game_over(self):
        # print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()
