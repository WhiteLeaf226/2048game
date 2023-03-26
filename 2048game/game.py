import random
import sys
import numpy
import pygame

class game():

    #初始化函数
    def __init__(self,width,height,block_jiange,block_size):
        self.width = width  #窗口宽
        self.height = height  #高
        self.block_jiange = block_jiange  #方块间隙
        self.block_size = block_size  #大小

        self.size = 4  # 列表 4 * 4
        self.a_lsit = []  # 初始化列表
        self.game_form = ""

        self.is_over = False  # 游戏是否结束
        self.is_victory = False  # 游戏是否成功
        self.score = 0  # 分数
        self.is_shengcheng_num = True  # 是否添加数字

        #方块颜色
        self.block_color = {  
            0: (205, 245, 244),
            2: (146, 244, 243),
            4: (0, 220, 244),
            8: (0, 167, 245),
            16: (115, 160, 253),
            32: (0, 121, 226),
            64: (47, 80, 147),
            128: (4, 66, 229),
            256: (98, 84, 219),
            512: (165, 128, 234),
            1024: (176, 99, 255),
            2048: (158, 0, 233)
        } 
        #数字颜色
        self.num_color = {
            0: (255, 255, 255),
            2: (255, 255, 255),
            4: (255, 255, 255),
            8: (255, 255, 255),
            16: (255, 255, 255),
            32: (255, 255, 255),
            64: (255, 255, 255),
            128: (255, 255, 255),
            256: (255, 255, 255),
            512: (255, 255, 255),
            1024: (255, 255, 255),
            2048: (255, 255, 255)
        } 

        self.biaoti_font = ""  # 窗口标题字体类型及大小: 2048
        self.score_font = ""  # 分数字体类型及大小
        self.shuoming_font = "" # 说明字体类型及大小
        self.shuzi_font = ""  # 数字字体

    #界面模块
    def Form(self):
        
        #初始化pygame
        pygame.init()

        #设置窗口大小和标题
        self.game_form = pygame.display.set_mode((self.width,self.height),0,0)
        pygame.display.set_caption("2048")

        #初始化游戏
        self.init_game()

        while True:

            self.huizhi_from()
            self.yonghu_caozuo()
            pygame.display.flip() #更新屏幕内容

    #判断用户操作
    def yonghu_caozuo(self):

        for event in pygame.event.get():
            #判断鼠标是否点击“x”按钮
            if event.type == pygame.QUIT:
                sys.exit()
            #判断键盘是否按下
            elif event.type == pygame.KEYDOWN:
                #重新开始游戏
                if event.key == pygame.K_ESCAPE:
                    self.init_game()  # 游戏初始化
    
                # ↑ 
                if event.key == pygame.K_UP and self.is_over == False and self.is_victory == False:
                    self.move_up()
        
                # ↓ 
                if event.key == pygame.K_DOWN and self.is_over == False and self.is_victory == False:
                    self.move_down()
    
                # ←
                if event.key == pygame.K_LEFT and self.is_over == False and self.is_victory == False:
                    self.move_left()
    
                # → 
                if event.key == pygame.K_RIGHT and self.is_over == False and self.is_victory == False:
                    self.move_right()

    #初始化游戏
    def init_game(self):
        self.score = 0;
        self.is_over = False
        self.is_victory = False
        #初始化列表并使初值为0
        self.a_list = numpy.zeros([self.size,self.size])

        for i in range(2):
            self.is_shengcheng_num = True
            self.shengcheng_num()
    
    #生成数字
    def shengcheng_num(self):
        a1_list = self.get_empty()
        if a1_list and self.is_shengcheng_num:

            #生成2的概率为3/5，4为2/5
            rand = random.randint(1,5)
            if rand % 5 == 4 or rand % 5 == 5:
                a = 4
            else:
                a = 2
            
            #从a1_list中选取一个独立的元素
            x,y = random.sample(a1_list, 1)[0]
            #生成数字
            self.a_list[x][y] = a

            self.is_shengcheng_num = False

    #获取空位
    def get_empty(self):
        a1_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.a_list[i][j] == 0:
                    a1_list.append([i,j])

        return a1_list

    #向上移动
    def move_up(self):
        
        for y in range(4):
            x1 = 0
            for x in range(1,4):
                if self.a_list[x][y] != 0:
                    #相同合并，累计分数。
                    if self.a_list[x][y] == self.a_list[x1][y]:
                        self.score += self.a_list[x][y] + self.a_list[x1][y]
                        self.a_list[x1][y] = self.a_list[x][y] + self.a_list[x1][y]
                        self.a_list[x][y] = 0
                        x1 += 1
                        self.is_shengcheng_num = True
                    #为零上移，分数不变
                    elif self.a_list[x1][y] == 0:
                        self.a_list[x1][y] = self.a_list[x][y]
                        self.a_list[x][y] = 0
                        self.is_shengcheng_num = True
                    #不同上移，分数不变
                    else:
                        #相邻不变
                        if x1 + 1 == x:
                            x1 += 1
                            continue
                        #相隔上移
                        else:
                            self.a_list[x1 + 1][y] = self.a_list[x][y]
                            self.a_list[x][y] = 0
                            self.is_shengcheng_num = True
                            x1 += 1
                       
    #向下移动
    def move_down(self):
        
        for y in range(4):
            x1 = 3
            #从 2 到 0 前闭后开输出 2 1 0
            for x in range(2, -1, -1):
                if self.a_list[x][y] != 0:
                    #相同合并，累计分数。
                    if self.a_list[x][y] == self.a_list[x1][y]:
                        self.score += self.a_list[x][y] + self.a_list[x1][y]
                        self.a_list[x1][y] = self.a_list[x][y] + self.a_list[x1][y]
                        self.a_list[x][y] = 0
                        x1 -= 1
                        self.is_shengcheng_num = True
                    #为零下移，分数不变
                    elif self.a_list[x1][y] == 0:
                        self.a_list[x1][y] = self.a_list[x][y]
                        self.a_list[x][y] = 0
                        self.is_shengcheng_num = True
                    #不同下移，分数不变
                    else:
                        #相邻不变
                        if x1 - 1 == x:
                            x1 -= 1
                            continue
                        #相隔下移
                        else:
                            self.a_list[x1 - 1][y] = self.a_list[x][y]
                            self.a_list[x][y] = 0
                            self.is_shengcheng_num = True
                            x1 -= 1

    #向左移动
    def move_left(self):

        for x in range(4):
            y1 = 0
            for y in range(1,4):
                if self.a_list[x][y] != 0:
                    #相同合并，累计分数。
                    if self.a_list[x][y] == self.a_list[x][y1]:
                        self.score += self.a_list[x][y] + self.a_list[x][y1]
                        self.a_list[x][y1] = self.a_list[x][y] + self.a_list[x][y1]
                        self.a_list[x][y] = 0
                        y1 += 1
                        self.is_shengcheng_num = True
                    #为零左移，分数不变
                    elif self.a_list[x][y1] == 0:
                        self.a_list[x][y1] = self.a_list[x][y]
                        self.a_list[x][y] = 0
                        self.is_shengcheng_num = True
                    #不同左移，分数不变
                    else:
                        #相邻不变
                        if y1 + 1 == y:
                            y1 += 1
                            continue
                        #相隔左移
                        else:
                            self.a_list[x][y1 + 1] = self.a_list[x][y]
                            self.a_list[x][y] = 0
                            self.is_shengcheng_num = True
                            y1 += 1
    
     #向右移动
    def move_right(self):

        for x in range(4):
            y1 = 3
            for y in range(2, -1, -1):
                if self.a_list[x][y] != 0:
                    #相同合并，累计分数。
                    if self.a_list[x][y] == self.a_list[x][y1]:
                        self.score += self.a_list[x][y] + self.a_list[x][y1]
                        self.a_list[x][y1] = self.a_list[x][y] + self.a_list[x][y1]
                        self.a_list[x][y] = 0
                        y1 -= 1
                        self.is_shengcheng_num = True
                    #为零右移，分数不变
                    elif self.a_list[x][y1] == 0:
                        self.a_list[x][y1] = self.a_list[x][y]
                        self.a_list[x][y] = 0
                        self.is_shengcheng_num = True
                    #不同右移，分数不变
                    else:
                        #相邻不变
                        if y1 - 1 == y:
                            y1 -= 1
                            continue
                        #相隔右移
                        else:
                            self.a_list[x][y1 - 1] = self.a_list[x][y]
                            self.a_list[x][y] = 0
                            self.is_shengcheng_num = True
                            y1 -= 1

    #判断游戏结束
    def game_over(self):

        a2_list = self.get_empty()
        #有空位不结束
        if a2_list:
            return False
        for x in range(3):
            for y in range(3):
                #判断相邻，两个数是否相等
                if self.a_list[x][y] == self.a_list[x][y + 1]:
                    return False
                if self.a_list[x][y] == self.a_list[x + 1][y]:
                    return False
        return True
    
    #判断游戏胜利
    def game_victory(self):
        if self.a_list.max() == 2048:
            return True
        return False

    #绘制界面
    def huizhi_from(self):

        #设置背景色
        self.game_form.fill((213,255,254))
        #初始化字体模块
        pygame.font.init()

        """添加标题"""
        pygame.draw.rect(self.game_form,(62,203,210),(0,0,600,200))
        self.biaoti_font = pygame.font.SysFont("幼圆",70,True)
        biaoti_name = self.biaoti_font.render("2048",True,(255,255,255))
        self.game_form.blit(biaoti_name,(50,10))

        """添加分数"""
        jvxing_chang = 200
        jvxing_kuang = 150
        #添加一个矩形区域
        pygame.draw.rect(self.game_form,(130,218,220),(300,25,jvxing_chang,jvxing_kuang))
        #设置字体、颜色和位置
        self.score_font = pygame.font.SysFont("SimHei",40,True)
        score_name = self.score_font.render("分数",True,(255,255,255))
        self.game_form.blit(score_name,(355,50))
        #设置颜色和位置
        score_count = self.score_font.render(str(int(self.score)),True,(255,255,255))
        self.game_form.blit(score_count,(275+jvxing_chang/2,30+jvxing_kuang/2))

        """添加游戏说明"""
        self.shuoming_font = pygame.font.SysFont("SimHei",20,True)
        shuoming1 = self.shuoming_font.render("操作：↑ ↓ ← →",True,(255,255,255))
        shuoming2 = self.shuoming_font.render("按esc键重新开始游戏",True,(255,255,255))
        self.game_form.blit(shuoming1,(25,80))
        self.game_form.blit(shuoming2,(25,120))
        
        """绘制方格"""
        for i in range(4):
            for j in range(4):
                #方块初始位置
                block_x = j * self.block_size + (j + 1) * self.block_jiange
                block_y = i * self.block_size + (i + 1) * self.block_jiange 

                count = int(self.a_list[i][j])
                if count == 0:
                    pygame.draw.rect(self.game_form,self.block_color[count],(block_x + 5,block_y + 210,self.block_size,self.block_size))
                else:
                    pygame.draw.rect(self.game_form,(164,196,195),(block_x + 13,block_y + 218,self.block_size,self.block_size))
                    pygame.draw.rect(self.game_form,self.block_color[count],(block_x + 5,block_y + 210,self.block_size,self.block_size))

                
                #数字字体及大小
                if 0 < count < 10:
                    self.shuzi_font = pygame.font.SysFont("SimHei",46,True)
                    count_name = self.shuzi_font.render(str(count),True,self.num_color[count])
                    self.game_form.blit(count_name,(block_x + 52,block_y + 245))
                    pass
                elif 10 < count < 100:
                    self.shuzi_font = pygame.font.SysFont("SimHei",40,True)
                    count_name = self.shuzi_font.render(str(count),True,self.num_color[count])
                    self.game_form.blit(count_name,(block_x + 42,block_y + 245))
                    pass
                elif 100 < count < 1000:
                    self.shuzi_font = pygame.font.SysFont("SimHei",34,True)
                    count_name = self.shuzi_font.render(str(count),True,self.num_color[count])
                    self.game_form.blit(count_name,(block_x + 32,block_y + 245))
                    pass
                elif count > 1000:
                    self.shuzi_font = pygame.font.SysFont("SimHei",28,True)
                    count_name = self.shuzi_font.render(str(count),True,self.num_color[count])
                    self.game_form.blit(count_name,(block_x + 22,block_y + 245))

        self.shengcheng_num()

        """ 如果游戏结束 """
        self.is_over = self.game_over()
        if self.is_over:
            over_font = pygame.font.SysFont("SimHei", 60, True)
            over_name = over_font.render('Game Over!', True, (0, 0, 0))
            self.game_form.blit(over_name, (130, 430))
 
        """ 如果游戏成功 """
        self.is_victory = self.game_victory()
        if self.is_victory:
            victory_font = pygame.font.SysFont("SimHei", 60, True)
            victory_name = victory_font.render('Successful!', True, (0, 0, 0))
            self.game_form.blit(victory_name, (130, 430))

