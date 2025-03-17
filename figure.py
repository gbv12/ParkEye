#coding = utf-8
import os
import time
import matplotlib.pyplot as plt # pip install matplotlib
import ocrutil # 导入自定义模块
import btn # 导入自定义模块
import pygame # 第三方模块  pip install pygame
import cv2 # 第三方模块 pip install opencv-python
import pandas as pd
import timeutil

total = 10#总车位

txt1=' '
txt2=' '
txt3=' '
pi_table=pd.read_excel('./datafile/停车场车辆表.xlsx')
pi_info=pd.read_excel('./datafile/停车场信息表.xlsx')
#计算停车场当前车辆数量
cars=pi_table[['carnumber','date','state']].values
carn = len(cars)
# print((type(cars)))
# print(cars)
def init_opencv():
    #初始化摄像机
    try:
        cam = cv2.VideoCapture(0)  #表示是第几个摄像机
    except:
        print("请确认摄像机是否连接")
    #success表示是否摄像机读取到，True/False
    success,img=cam.read()
    # print(success)
    #保存图片
    cv2.imwrite('./file/test.jpg',img)
    #加载图片
    image = pygame.image.load('./file/test.jpg')
    image=pygame.transform.scale(image,(400,300))
    #放到屏幕中显示
    screen.blit(image,(2,2))
def save_data():
    cdir = os.getcwd()#获取当前python文件的路径
    #拼接文件保存的路径
    path = cdir +"/datafile/"
    #判断路径是否存在，不存在测创建
    if not os.path.exists(path+"停车场车辆表.xlsx"):
        os.makedirs(path)
        #创建一个dateframe对象
        carfile = pd.DataFrame(columns=['carnumber','date','price','state'])
        carfile.to_excel(path+"停车场车辆表.xlsx",sheet_name='data',index=False)
        carfile.to_excel(path+"停车场信息表.xlsx",sheet_name='data',index=False)

def text0(screen):
    pygame.draw.rect(screen,BG,(420,2,260,420))
    # 在矩形中画一条横线  参数中的1，是为了解决旧版本pygame
    pygame.draw.aaline(screen,GREEN,(415,40),(690,40),1)
    # 绘制信息框
    pygame.draw.rect(screen,GREEN,(400,260,270,120),1)
    # 使用字体
    xtfont=pygame.font.SysFont('SimHei',20)
    # 将文字转成图片
    textstart=xtfont.render('信息',True,GREEN)
    # 获取文字图像的矩形大小
    text_rect=textstart.get_rect()
    # 设置文字图像的中心点
    text_rect.centerx=430
    text_rect.centery=275
    screen.blit(textstart,text_rect)

def text1(screen):
    k=total-len(cars)
    if k<10 :
        sk = '0' + str(k)
    else:
        sk=str(k)
    xtfont=pygame.font.SysFont('SimHei',20)
    textstart=xtfont.render(f'一共有车位：{total}，剩余车位：{sk}',True,WHITE)
    #获取图片中心点
    text_rect = textstart.get_rect()
    text_rect.centerx=550
    text_rect.centery=30
    #绘制到窗体中
    screen.blit(textstart,text_rect)
#停车场信息表头
def text2(screen):
    xtfont = pygame.font.SysFont('SimHei',20)
    #将文字转成图片
    textstart=xtfont.render('车号        时间   ',True,WHITE)
    text_rect = textstart.get_rect()
    text_rect.centerx=500
    text_rect.centery=50
    screen.blit(textstart,text_rect)

#读取车辆信息
def text3(screen):
    xtfont = pygame.font.SysFont('SimHei', 20)
    # 将文字转成图片
    cars=pi_table[['carnumber','date','state']].values
    #最多显示十辆车
    if len(cars)>10 :
        cars=pd.read_excel('./datafile/停车场车辆表.xlsx',sheet_name='data',skiprows=len(cars)-10)
    n=0
    for car in cars :
        n=n+1
        textstart = xtfont.render(str(car[0])+' '+str(car[1]), True, WHITE)
        text_rect = textstart.get_rect()
        text_rect.centerx = 530
        text_rect.centery = 70+20*n
        screen.blit(textstart,text_rect)

def text4(screen,txt1,txt2,txt3):
    # 使用系统字体
    xtfont=pygame.font.SysFont('SimHei',15)
    texttxt1=xtfont.render(txt1,True,GREEN)
    # 获取文字图像的位置
    text_rect=texttxt1.get_rect()
    text_rect.centerx=533
    text_rect.centery=318
    # 绘制内容
    screen.blit(texttxt1,text_rect)

    # 第二条信息
    texttxt2 = xtfont.render(txt2, True, GREEN)
    # 获取文字图像的位置
    text_rect = texttxt2.get_rect()
    text_rect.centerx = 533
    text_rect.centery = 318 + 20
    # 绘制内容
    screen.blit(texttxt2, text_rect)

    # 第三条信息
    texttxt3 = xtfont.render(txt3, True, GREEN)
    # 获取文字图像的位置
    text_rect = texttxt3.get_rect()
    text_rect.centerx = 533
    text_rect.centery =318 + 40
    # 绘制内容
    screen.blit(texttxt3, text_rect)
    # # 满预警提示(明天讲） 为什么要获取state为2的，因为state=2表示没有余位
    # kcar=pi_info_table[pi_info_table['state']==2]
    # kcars=kcar['date'].values
    # week_number=0 # 0表示星期一 ，星期五是数字4 ，假设星期日车位比较紧张
    # for k in kcars: # k 是日期
    #     # 计算星期几? k是字符串类型
    #     week_number=timeutil.get_week_number(k)
    #
    #     # 今天的是星期几?
    #     localtime=time.gmtime().tm_wday
    #
    #
    #     if week_number==4: #5表示星期六
    #         if localtime==4:
    #             text6(screen,'根据数据分析，明天可能出现车位紧张的情况，请做好调度!')
    #         elif localtime==5: # 如果今天已经是星期六
    #             text6(screen,'根据数据分析，今天可能出现车位紧张的情况，请做好调度！')
    #     else:
    #         if localtime==5:
    #             text6(screen, '根据数据分析，今天可能出现车位紧张的情况，请做好调度！')


size = 700,400

#帧率
FPS = 30
#背景颜色
BG = (73,39,25)
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,232,0)
BLUE=(72,61,139)
GARY=(96,96,96)

#初始化pygame 运行框
pygame.init()
#设置窗体名称及大小背景
pygame.display.set_caption("智能停车场系统")
screen=pygame.display.set_mode(size)
screen.fill(BG)
clock = pygame.time.Clock()
#开启摄像头
init_opencv()
save_data()

#主线程
Running = True
while Running:
    pi_table = pd.read_excel('./datafile/停车场车辆表.xlsx')
    pi_info = pd.read_excel('./datafile/停车场信息表.xlsx')
    #初始化按钮对象
    button = btn.Button(screen,(400,390),150,40,BLUE,WHITE,'识别',25)
    #将按钮绘制到窗口
    button.draw_button()
    text0(screen)
    text1(screen)
    text2(screen)
    text3(screen)
    text4(screen,txt1,txt2,txt3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos();#返回的是元组
            print(mouse_pos)
            if mouse_pos[0]>=250 and mouse_pos[0]<=400 and 350<=mouse_pos[1]<=390:
                print("点击识别")#点击按钮调用识别车牌
                try:
                    carnum=ocrutil.getcn()
                    print(carnum)
                    #进入停车场或者出停车场
                    localtime = time.localtime()
                    carsk = pi_table['carnumber'].values
                    if carnum in carsk:
                        txt1='车牌号:'+carnum
                        # 计算时间差
                        y=0
                        #获取行数 (行索引)出停车要删除的那个车辆的行索引
                        kcar=0
                        # 从Excel文件中获取数据
                        cars=pi_table[['carnumber','date','state']].values # Numpy中的数组类型
                        #循环数据
                        for car in cars: # 获取一辆车
                            if carnum==car[0]: #
                                #计算时间差
                                y=timeutil.DtCale(car[1],localtime)
                                break
                            kcar+=1 # 如果当前这辆车不是要出停车场车
                        txt3 = '出停车场时间:' + time.strftime('%Y-%m-%d %H:%M', localtime)
                        pi_table = pi_table.drop(kcar, axis=0)
                        # 保存信息到Excel文件中
                        pi_table.to_excel('./datafile/停车场车辆表.xlsx', sheet_name='data', index=False, header=True)
                        carn -= 1  # 出停车场一辆车，车的数量要减少1
                        pi_info = pi_info._append(
                            {'carnumber': carnum, 'date': time.strftime('%Y-%m-%d %H:%M', localtime), 'price': 3 * y,
                             'state': 1},
                            ignore_index=True)
                        pi_info.to_excel('./datafile/停车场信息表.xlsx', sheet_name='data', index=False,
                                               header=True)
                    else:
                        #判断停车场是否有余位
                        if carn < total:
                            pi_table = pi_table._append(
                                {'carnumber': carnum, 'date': time.strftime('%Y-%m-%d %H:%M', localtime), 'state': 0},
                                ignore_index=True)
                            # 数据添加完成，把table储存到文件中
                            pi_table.to_excel("./datafile/停车场车辆表.xlsx", sheet_name='data', index=False, header=True)
                            #
                            # pi_info = pi_info._append(
                            #     {'carnumber': carnum, 'date': time.strftime('%Y-%m-%d %H:%M', localtime), 'state': 0},
                            #     ignore_index=True)
                            # pi_info.to_excel("./datafile/停车场信息表.xlsx", sheet_name='data', index=False, header=True)
                            print("数据保存成功")
                            carn+=1
                            txt1='车牌号'+carnum
                            txt2='有空余车位，可以进入停车场'
                            txt3='进入停车场时间 '+ str(time.strftime('%Y-%m-%d %H:%M', localtime))
                        else:
                            pi_info = pi_info._append(
                                {'carnumber': carnum, 'date': time.strftime('%Y-%m-%d %H:%M', localtime),
                                 'state': 2}, ignore_index=True)
                            pi_info.to_excel('./datafile/停车场信息表.xlsx', sheet_name='data', index=False,
                                                   header=True)
                            txt1 = '车牌号:' + carnum
                            txt2 = '没有空余车位，不可以进入停车场'
                            txt3 = '时间:' + str(time.strftime('%Y-%m-%d %H:%M', localtime))

                except:
                    print("识别失败")
                    continue
        #更新界面
        pygame.display.flip()
        clock.tick(FPS)#控制循环的执行时间

