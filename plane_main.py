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
        pygame.time.set_timer(CREATE_ENEMY_EVENT,500)
        pygame.time.set_timer(HERO_FIRE_EVENT, 400)
        pygame.time.set_timer(CREATE_ENEMY2_EVENT, 2000)
        # pygame.time.set_timer(CREATE_ENEMY3_EVENT, 1000)
        # 5. 记分牌
        self.count_die_enemy = 0
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
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出场")
                enemy = Enemy()
                # enemy2 = Enemy2()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            elif event.type == CREATE_ENEMY2_EVENT:
                # print("敌机2出场")
                enemy2 = Enemy()
                enemy2.image=pygame.image.load("./images/enemy2.png")
                self.enemy_group.add(enemy2)
            # elif event.type == CREATE_ENEMY3_EVENT:
            #     # print("敌机3出场")
            #     enemy3 = Enemy()
            #     enemy3.image=pygame.image.load("./images/enemy3_n1.png")
            #     enemy3.speed = 1
                #将敌机精灵添加到敌机精灵组
                # self.enemy_group.add(enemy3)
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 3
            self.hero.goto = 1
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -3
            self.hero.goto = 1
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed = -3
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
        # 2.敌机撞毁英雄-这里会返回精灵组的一个列表-如果没有发生碰撞，列表为空列表
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(enemies) >0:
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

    # 可以指定循环体内部的代码执行的频率


if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()

