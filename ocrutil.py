#coding:utf-8
#车牌识别系统（小项目）实现项目的核心功能
# https://ai.baidu.com/  百度AI开放平台
# 安装  pip install baidu-aip
# baidu-aip 是百度AI开发平台的Python SDK(软件开发工具包)
# 安装 pip install chardet 用于检测文本文件或二进制数据流的字符编码库
from aip import AipOcr   #OCR 光学字符识别
# 以下常量的值，需要到百度开放平台去注册，创建应用

def get_file_content(filepath):# 函数的定义
    with open(filepath,'rb') as file: # 上下文管理器，文件的读取,读取的模式是rb，读取字节类型
       return  file.read() # 读取全部字节并返回

APP_ID='94190102'
API_KEY='v0RXcCRYISrWm67tWbxXfqHZ'
SECRET_KEY='j7r8oaxYGhnnRhqIZRHmunVBcyoK28wS'

# 面向对象
client=AipOcr(APP_ID,API_KEY,SECRET_KEY)

# 根据图片，返回车牌号
def getcn():
    # 读取图片
    image=get_file_content('./file/test.jpg')
    # 调用车牌识别
    results=client.licensePlate(image) # 对象名.方法名()
    # print(type(results),results)  # dict字典类型
    # 字典取值  results['words_result']结果也是字典类型
    # 字典取值有两种方式  字典名称[key]   第二种方式  字典名称.get(key)
    return results['words_result']['number'] # 函数的返回值在33行被输出
if __name__ == '__main__':
    print(getcn())