#coding:utf-8
import os
import time
import matplotlib.pyplot as plt # pip install matplotlib
import ocrutil # 导入自定义模块
import btn # 导入自定义模块
import pygame # 第三方模块  pip install pygame
import cv2 # 第三方模块 pip install opencv-python
import pandas as pd
import timeutil
# 定义一个函数
def init_opencv():
    # 初始化摄像头
    try:
        cam=cv2.VideoCapture(0) #0表示的是第一个摄像头
    except:
        print('请连接摄像头')
    # 从摄像头去读取图片
    sucess,img=cam.read() # sucess表示调用摄像头是否成功，True，False
    print(sucess)
    if sucess:
        # 保存图片，退出
        cv2.imwrite('./file/test.jpg',img) # img具体的图像数据
        # 加载图像
        image=pygame.image.load('./file/test.jpg')
        # 设置一下图片的大小
        image=pygame.transform.scale(image,(640,480))
        # 将图片放到屏幕中显示
        screen.blit(image,(2,2)) # (2,2)图片左上在窗体中的坐标

# 数据保存
def save_data():   # current  work  directory
    cdir=os.getcwd() # 获取当前的工作路径，当前py文件的位置
    # 拼接文件保存的路径
    path=cdir+'/datafile/'
    # 判断路径是否存在，路径不存创建
    if not os.path.exists(path+'停车场车辆表.xlsx'):
        # 创建文件夹
        os.makedirs(path) # 创建多级路径 ,如果父目录datafile不存在，则一同创建
        # 创建一个DataFrame对象
        # 车牌号，日期时间， 价格， 状态
        carnfile=pd.DataFrame(columns=['carnumber','date','price','state'])
        # 生成excel文件
        carnfile.to_excel(path+'停车场车辆表.xlsx',sheet_name='data',index=False)
        carnfile.to_excel(path+'停车场信息表.xlsx',sheet_name='data',index=False)


total=3 # 表示有100个停车位
txt1=''
txt2=''
txt3=''
income_switch=False # 收入统计计算的开关
# 获取当前停车场停车的数量
pi_table=pd.read_excel('./datafile/停车场车辆表.xlsx',sheet_name='data')
pi_info_table=pd.read_excel('./datafile/停车场信息表.xlsx',sheet_name='data')
# 停车场停了多少量车
cars=pi_table[['carnumber','date','state']].values
# cars是什么数据类型
#print(type(cars)) # Numpy中的数组类型
#print(cars) # 类似于Python语法中的二维列表
carn=len(cars)
print(carn)
# 背景文案图
def text0(screen):
    pygame.draw.rect(screen,BG,(650,2,350,640))
    # 在矩形中画一条横线  参数中的1，是为了解决旧版本pygame
    pygame.draw.aaline(screen,GREEN,(600,50),(980,50),1)
    # 绘制信息框
    pygame.draw.rect(screen,GREEN,(650,350,342,85),1)
    # 使用字体
    xtfont=pygame.font.SysFont('SimHei',20)
    # 将文字转成图片
    textstart=xtfont.render('信息',True,GREEN)
    # 获取文字图像的矩形大小
    text_rect=textstart.get_rect()
    # 设置文字图像的中心点
    text_rect.centerx=675
    text_rect.centery=365
    screen.blit(textstart,text_rect)
   # pi_table是在第50行进行的数据读取 pi_table是dataframe类型
    # 计算停的时间最长的车
    cars=pi_table[['carnumber','date','state']].values # numpy中的数组类型
    if len(cars)>0:
        longcar=cars[0][0] # 二维数组取值
        cartime=cars[0][1]
        # 使用系统字体
        xtfont=pygame.font.SysFont('SimHei',18)
        # 计算时长
        htime=timeutil.DtCale(cartime,time.localtime())
        # 将文字转成矩形
        textscar=xtfont.render(f'停车时间最长的车辆:{str(longcar)}',True,RED)
        texttime=xtfont.render(f'已停车:{str(htime)}小时',True,RED)
        text_rect1=textscar.get_rect()
        text_rect2=texttime.get_rect()
        # 设置图片的中心点
        text_rect1.centerx=820
        text_rect1.centery=320
        text_rect2.centerx=820
        text_rect2.centery=335
        # 绘制内容
        screen.blit(textscar,text_rect1)
        screen.blit(texttime,text_rect2)

# 车位文本
def text1(screen):
    # 剩余车位
    k=total-carn
    if k<10:
        sk='0'+str(k)
    else:
        sk=str(k)
    # 使用系统字体
    xtfont=pygame.font.SysFont('SimHei',30)
    #将文字转成图片
    textstart=xtfont.render(f'一共有车位:{total},剩余车位:{sk}',True,WHITE)
    # 获取文字转成图片之后的矩形的大小
    text_rect=textstart.get_rect()
    # 设置文字图像的中心点
    text_rect.centerx=790
    text_rect.centery=30
    # 绘制到窗体中
    screen.blit(textstart,text_rect) # 车
# 停车场信息表头
def text2(screen):
    # 使用系统字体
    xtfont=pygame.font.SysFont('SimHei',20)
    # 将文字转成图片
    textstart=xtfont.render('车号     时间  ',True,WHITE)
    # 获取文字图片的矩形大小
    text_rect=textstart.get_rect()
    # 设置文字图像的中心点
    text_rect.centerx=730
    text_rect.centery=70
    # 绘制内容
    screen.blit(textstart,text_rect)
# 读取车辆信息
def text3(screen):
    # 使用的字体
    xtfont=pygame.font.SysFont('SimHei',20)
    cars=pi_table[['carnumber','date','state']].values
    # 页面中只绘制10辆车的信息
    if len(cars)>10:
        cars=pd.read_excel('./datafile/停车场车辆表.xlsx',sheet_name='data',skiprows=len(cars)-10)

    # 动态绘制y点坐标
    n=0  # 表示的是第几辆车
    for car in cars: # cars是二维数组 ，car 是一维数组
        n+=1
        # 将车牌和进入的时间转成一张图片
        textstart=xtfont.render(str(car[0])+'  '+str(car[1]),True,WHITE)
        # 获取文字图像的矩形
        text_rect=textstart.get_rect()
        # 设置文字图像的中心点
        text_rect.centerx=780
        text_rect.centery=70+30*n # 第一辆车y的中心点是100，第二辆是130..
        # 绘制到界面上
        screen.blit(textstart,text_rect)
# 历史信息及满预警信息
def text4(screen,txt1,txt2,txt3):
    # 使用系统字体
    xtfont=pygame.font.SysFont('SimHei',20)
    texttxt1=xtfont.render(txt1,True,GREEN)
    # 获取文字图像的位置
    text_rect=texttxt1.get_rect()
    text_rect.centerx=820
    text_rect.centery=355+20
    # 绘制内容
    screen.blit(texttxt1,text_rect)

    # 第二条信息
    texttxt2 = xtfont.render(txt2, True, GREEN)
    # 获取文字图像的位置
    text_rect = texttxt2.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 355 + 40
    # 绘制内容
    screen.blit(texttxt2, text_rect)

    # 第三条信息
    texttxt3 = xtfont.render(txt3, True, GREEN)
    # 获取文字图像的位置
    text_rect = texttxt3.get_rect()
    text_rect.centerx = 820
    text_rect.centery = 355 + 60
    # 绘制内容
    screen.blit(texttxt3, text_rect)
    # 满预警提示(明天讲） 为什么要获取state为2的，因为state=2表示没有余位
    kcar=pi_info_table[pi_info_table['state']==2]
    kcars=kcar['date'].values
    week_number=0 # 0表示星期一 ，星期五是数字4 ，假设星期日车位比较紧张
    for k in kcars: # k 是日期
        # 计算星期几? k是字符串类型
        week_number=timeutil.get_week_number(k)

        # 今天的是星期几?
        localtime=time.gmtime().tm_wday


        if week_number==4: #5表示星期六
            if localtime==4:
                text6(screen,'根据数据分析，明天可能出现车位紧张的情况，请做好调度!')
            elif localtime==5: # 如果今天已经是星期六
                text6(screen,'根据数据分析，今天可能出现车位紧张的情况，请做好调度！')
        else:
            if localtime==5:
                text6(screen, '根据数据分析，今天可能出现车位紧张的情况，请做好调度！')



# 收费图表的展示
def text5(screen):
    #计算price列的和
    sum_price=pi_info_table['price'].sum()
    #使用系统字体
    xtfont=pygame.font.SysFont('SimHei',20)
    #将文字转成图片
    textstart=xtfont.render(f'共计收入:{str(sum_price)}元',True,WHITE)
    # 获取文字图片的矩形
    text_rect=textstart.get_rect()
    # 设置图片文字的中心点
    text_rect.centerx=1200
    text_rect.centery=30
    # 绘制内容
    screen.blit(textstart,text_rect)
    # 加载图片
    image=pygame.image.load('./file/income.png')
    # 设置图片的大小
    image=pygame.transform.scale(image,(390,430))
    # 绘制月份收入图片
    screen.blit(image,(1000,50))

def text6(screen,week_info):
    pygame.draw.rect(screen,YELLOW,((2,2),(640,40)))
    xtfont=pygame.font.SysFont('SimHei',20)
    #将文本转成图片
    textstart=xtfont.render(week_info,True,RED)
    #获取文本图片的矩形
    text_rect=textstart.get_rect()
    # 设置文本图像的中心点
    text_rect.centerx=322
    text_rect.centery=20
    # 绘制到界面上
    screen.blit(textstart,text_rect)
 # 窗体的大小
size=1000,484  # size是元组类型
#帧率
FPS=60
# 背景色
BG=(73,119,142) # 背景色是一个元组，颜色自己定

''' 定义背景颜色'''
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
BLUE=(72,61,139)
GARY=(96,96,96)
RED=(220,20,60)
YELLOW=(255,255,0)
# 初始化pgame
pygame.init()
#设置窗体的名称
pygame.display.set_caption('智能停车场车牌识别计费系统')
# 设置窗体的大小
screen=pygame.display.set_mode(size)
#填充背景颜色
screen.fill(BG)
#创建一个钟表
clock=pygame.time.Clock()
# 调用调用摄像头的函数

save_data()
#主线程
Running=True  #18602218136 企微
while Running:
    #init_opencv()
    pi_table = pd.read_excel('./datafile/停车场车辆表.xlsx', sheet_name='data')
    pi_info_table = pd.read_excel('./datafile/停车场信息表.xlsx', sheet_name='data')
    # 停车场停了多少量车
    cars = pi_table[['carnumber', 'date', 'state']].values

    text0(screen)
    text1(screen) # 车位文字
    text2(screen) # 车位信息的表头
    text3(screen) # 车辆信息
    text4(screen,txt1,txt2,txt3)
    text5(screen)
    # 初始化按钮对象
    button_go=btn.Button(screen,(640,480),150,60,BLUE,WHITE,'识别',25)
    # 将按钮绘制到窗体上
    button_go.draw_button()
    # 创建按钮对象， 收入统计
    button_go1=btn.Button(screen,(990,480),100,40,RED,WHITE,'收入统计',25)
    #将按钮绘制到窗体上
    button_go1.draw_button()

    # 获取键盘事件
    for event in pygame.event.get():
        # 窗体关闭应用程序就关闭
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos() # 结果是元组(x,y)
            # 492=640-150+2
            if 492<=mouse_pos[0] and mouse_pos[0]<=642 and 422<=mouse_pos[1]  and mouse_pos[1]<=482:
                print('点击识别') # 点击“识别”按钮时，调用识别车牌的模块，识别摄像头照下来的照片中的车牌号码
                try:
                    carnumber=ocrutil.getcn()
                    print(carnumber)
                    # 进入停车场还是要出停车场
                    localtime=time.localtime() # 获取当前系统时间
                    #获取Excel文件中车牌那列的数据
                    carsk=pi_table['carnumber'].values # numpy中的ndarray类型
                    #当前被点击识别的这辆车，是否在 停车场车辆的一维数据中
                    if carnumber in carsk: # if中的代码是结算的过程,出停车场
                        txt1='车牌号:'+carnumber
                        # 计算时间差
                        y=0
                        #获取行数 (行索引)出停车要删除的那个车辆的行索引
                        kcar=0
                        # 从Excel文件中获取数据
                        cars=pi_table[['carnumber','date','state']].values # Numpy中的数组类型
                        #循环数据
                        for car in cars: # 获取一辆车
                            if carnumber==car[0]: #
                                #计算时间差
                                y=timeutil.DtCale(car[1],localtime)
                                break
                            kcar+=1 # 如果当前这辆车不是要出停车场车，行索引要加

                        if y==0:
                            y=1 # 不到1小时按1小时收费
                        txt2='停车费:'+str(3*y)+'元'
                        txt3='出停车场时间:'+time.strftime('%Y-%m-%d %H:%M',localtime)
                        # 出停车场，停车数据要从Excel文件中删除
                        pi_table=pi_table.drop(kcar,axis=0)
                        # 保存信息到Excel文件中
                        pi_table.to_excel('./datafile/停车场车辆表.xlsx',sheet_name='data',index=False,header=True)
                        carn-=1 #出停车场一辆车，车的数量要减少1
                        pi_info_table = pi_info_table._append(
                            {'carnumber': carnumber, 'date': time.strftime('%Y-%m-%d %H:%M', localtime),'price':3*y, 'state': 1},
                            ignore_index=True)
                        pi_info_table.to_excel('./datafile/停车场信息表.xlsx', sheet_name='data', index=False,
                                               header=True)

                    else: # 进入停车场
                        # 判断停车场是否有余位
                        if carn<total: # 说明有余位
                            #需要向Excel文件中增加一条数据
                            pi_table=pi_table._append({'carnumber':carnumber,'date':time.strftime('%Y-%m-%d %H:%M',localtime),'state':0},ignore_index=True)
                            pi_table.to_excel('./datafile/停车场车辆表.xlsx',sheet_name='data',index=False,header=True)
                            pi_info_table = pi_info_table._append(
                                {'carnumber': carnumber, 'date': time.strftime('%Y-%m-%d %H:%M', localtime),
                                 'state': 0}, ignore_index=True)
                            pi_info_table.to_excel('./datafile/停车场信息表.xlsx', sheet_name='data', index=False,
                                              header=True)
                            carn+=1
                            txt1='车牌号:'+carnumber
                            txt2='有空余车位,可以进入停车场'
                            txt3='进停车场时间:'+time.strftime('%Y-%m-%d %H:%M', localtime)

                        else:  # 没有余位的情况 state取值，0，1，2， 0表示已进停车场 1表示出停车场 ，2表示没有车位
                            pi_info_table=pi_info_table._append({'carnumber':carnumber,'date':time.strftime('%Y-%m-%d %H:%M',localtime),'state':2},ignore_index=True)
                            pi_info_table.to_excel('./datafile/停车场信息表.xlsx',sheet_name='data',index=False,header=True)
                            txt1='车牌号:'+carnumber
                            txt2='没有空余车位，不可以进入停车场'
                            txt3='时间:'+str(time.strftime('%Y-%m-%d %H:%M',localtime))

                except:
                    print('识别出错')
                    continue
                # 鼠标获到这个范围内，说明点击了收入统计按钮
            elif 892<=mouse_pos[0] and mouse_pos[0]<=992 and 442<=mouse_pos[1] and mouse_pos[1]<=482:
                #print('收入统计按钮')
                if income_switch: #如果 income_switch值为True时
                    income_switch=False
                    #设置窗体的大小
                    size=1000,484
                    screen=pygame.display.set_mode(size)
                    screen.fill(BG)
                else:
                    income_switch=True
                    # 设置窗体的大小
                    size=1500,484
                    screen = pygame.display.set_mode(size)
                    screen.fill(BG)
                    attr=[str(i)+'月'for i in range(1,13)] # 柱状图的x轴上的数据
                    v1=[] # 用于存储y轴上数据， 每个月的停车费
                    for i in range(1,13): # 为什么要执行12次循环，因为有12个月
                        k=i
                        if i<10:
                            k='0'+str(k) # 为什么要凑位？
                        kk=pi_info_table[pi_info_table['date'].str.contains('2024-'+str(k))]
                        kk=kk['price'].sum()
                        v1.append(kk)
                    # 绘图，数据可视化 处理中文乱码
                    plt.rcParams['font.sans-serif']=['SimHei']
                    #设置柱状图图片的大小
                    plt.figure(figsize=(3.9,4.3)) # 单位英寸
                    # 绘制柱状图
                    plt.bar(attr,v1,0.5,color='green')
                    # 设置每根柱子上的数字标签
                    for a,b in zip(attr,v1): #a表示的是月份,b表示的是数值
                        plt.text(a,b,'%.0f'%b,ha='center',va='bottom',fontsize=7)
                    # 设置柱状图的标题
                    plt.title('每月收入统计')
                    #设置y轴的范围
                    plt.ylim((0,max(v1)+50))
                    plt.savefig('file/income.png')

    # 更新界面
    pygame.display.flip()
    clock.tick(FPS) # 帧频率  控制循环的执行时间
