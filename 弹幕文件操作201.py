#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from rich import print #一个颜色库
import re
import os
import time

def revise():#修正
    nr = files_name()
    print('''
    ==================================================================================
    \t\t\t\t[yellow]子\t菜\t单[/yellow]
    ==================================================================================
    * --> [1]. [green]更改[/green]>> 更改cid.(可以将本文件用于其他视频)

    * --> [2]. [green]修正[/green]>> 将弹幕文件修正为可识别的样子.(只修正)
    ==================================================================================
    \t[red]【注意】:[/red][yellow]BiliLocal 中本身就能识别任意视频弹幕文件,无需修改cid.[/yellow]
    ==================================================================================
    ''')
    xzz = xz(1,2)
    if xzz ==1:
        prtime('请输入 新的cid >>')
        cid = xz(0,999999999)
    if xzz == 2:
        cid = nr[2]
    wj = open(f'修正-{nr[1]}','w',encoding='utf-8')
    wj.writelines(f'<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>{cid}</chatid><mission>0</mission><maxlimit>1000</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>\n')
    for i in nr[0]:
        wj.writelines(i)
    wj.writelines('</i>')
    wj.close()
    prtime(f'输出文件[yellow][ 修正-{nr[1]} ][/yellow]完成! 文件共有弹幕 [yellow]{len(nr[0])}[/yellow] 条 , 本弹幕文件的视频cid为 [yellow]{cid}[/yellow] .')

def merge():#合并弹幕文件并查重
    while True:
        nr_1 = files_name()
        nr_2 = files_name()
        if nr_1 != nr_2:
            break
        prerr('不可以合并一个文件')
    dm_set = set(nr_1[0]) | set(nr_2[0]) #并集
    dm_list = list(dm_set)
    if nr_1[2] != nr_2[2]:
        prerr(f'判断到文件[{nr_1[1]}]与文件[{nr_2[1]}]所合并的视频cid不同.')
        prerr('检测到多个cid,请去[功能2]修复本文件!')
        cid = '314'
    cid = nr_1[2]
    wj = open(f'合并-{nr_1[1]}-{nr_2[1]}','w',encoding='utf-8')
    wj.writelines(f'<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>{cid}</chatid><mission>0</mission><maxlimit>1000</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>\n')
    for i in dm_list:
        wj.writelines(i)
    wj.writelines('</i>')
    wj.close()
    prtime(f'输出文件[ 合并-{nr_1[1]}-{nr_2[1]} ]完成! 文件共有弹幕 {len(dm_list)} 条 , 本弹幕文件的视频cid为 {cid} .')    

def find_duplicates():#查重
    nr = files_name()
    dm_set = set(nr[0])#转换为集合
    dm_list = list(dm_set)#转换为列表(顺序会变)
    wj = open(f'查重-{nr[1]}','w',encoding='utf-8')
    wj.writelines(f'<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>{nr[2]}</chatid><mission>0</mission><maxlimit>1000</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>\n')
    for i in dm_list:
        wj.writelines(i)
    wj.writelines('</i>')
    wj.close()
    prtime(f'输出文件[yellow][ 查重-{nr[1]} ][/yellow]完成! 文件共有弹幕 [yellow]{len(dm_list)}[/yellow] 条 , 本弹幕文件的视频cid为 [yellow]{nr[2]}[/yellow] .')
    

def files_name(): #输入文件后,获取文件内容,并且修正格式,还得到cid
    while True:
        try:
            wj_name = str(input('请输入要查重的弹幕文件(如 "弹幕文件.xml" ):'))
            with open(f'{wj_name}','r',encoding='UTF-8')as wj:
                wj_nr = wj.readlines() #获取文件每一行内容,保存为列表
            break
        except:
            prerr('请输入正确的文件名 + .xml')
    #匹配弹幕的正则表达式
    re_cid = re.compile(r'<chatid>(\d+)</chatid>')#抓取cid
    re_all = re.compile(r'(<d p="\d+\.\d+,\d,\d+,\d+,\d+,\d,.+?,\d+">.+?</d>)')#匹配弹幕
    #修复BUG高级弹幕
    re_ll_gjdm_t = re.compile(r'^(\[)\d+?,')#判断是否为高级弹幕 头部
    re_ll_gjdm_w = re.compile(r'",\d(])$')#尾部
    bug_gjdm = 0
    new_list = [] #搞到所有符合的弹幕的列表.(不带换行符 \n )
    v_cid = 'null'
    set_ = set()
    for x in wj_nr:
        dm_cid = set(re.findall(re_cid,x))
        if dm_cid != set_:#获取cid
            if len(dm_cid) == 1:
                if v_cid == 'null' or v_cid == list(dm_cid)[0]:
                    v_cid = list(dm_cid)[0]
                    prtime(f'获取到视频cid为 {v_cid}')
                else:
                    prerr('检测到多个cid,请去[功能2]修复本文件!')
            else:
                prerr('检测到多个cid,请去[功能2]修复本文件!A')
        new_list_preliminary = re.findall(re_all,x)#防止一行里面有很多弹幕
        for i in new_list_preliminary:
            dm_t = re.findall(re_ll_gjdm_t,i)
            dm_w = re.findall(re_ll_gjdm_w,i)
            if '[' in dm_t and']' in dm_w:
                danmu_nr = re.sub(r'(\\")','',i)
                prtime(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
                bug_gjdm+=1
            else:
                danmu_nr = i
            new_list.append(danmu_nr+'\n')
    prtime(f'修正完毕 , 共 {len(new_list)} 条弹幕 , 企图修正高级弹幕 {bug_gjdm} 条.')
    return new_list, wj_name, v_cid


def prtime(say):
    print(f'[green][{time.strftime("%H:%M:%S")}]:{say}[/green]')

def prerr(say):
    print(f'[red][{time.strftime("%H:%M:%S")}]【错误】:{say}[/red]')

def search():#初始化工作区
    re_ll_wj = re.compile(r'^(.:\\)')
    dq = os.getcwd()
    print("当前工作目录 : %s" % dq)
    name = 'HX定位文件' #填写文件名
    print(f'若不是您想要的工作目录,请在 [red]本盘工作目录区域[/red] 创建一个"[yellow]{name}[/yellow]"文件用于定位. ')
    path = re.findall(re_ll_wj,dq)[0]
    for root, dirs, files in os.walk(path):  # path 为根目录
    #root-路径 dirs-文件夹 files-文件
        if name in dirs or name in files:
            #flag = 1      判断是否找到文件
            root = str(root)
            os.chdir(os.path.join(root))
            print(f'[green]【成功找到文件!】初始化工作目录成功!\n当前工作目录: {os.getcwd()}[/green]')
            return
    print('[red]【错误】:找不到文件![/red]')
    return

def xz(m,x):#选择函数
    while True:
        try:
            print(f'[yellow]请输入 {m} ~ {x} 之间的数字.[/yellow]')
            xz=int(input('请选择:'))
            if m<=xz<=x:
                return xz
            else:
                print('请输入一个有效的数字!')
        except:
            print('错误数值!请按要求输入.')

def menu():#菜单
    print(r'''[green]
                    __/\\\________/\\\___/\\\_______/\\\_        
                    _\/\\\_______\/\\\__\///\\\___/\\\/__       
                    _\/\\\_______\/\\\____\///\\\\\\/____      
                    _\/\\\\\\\\\\\\\\\______\//\\\\______     
                    _\/\\\/////////\\\_______\/\\\\______    
                    _\/\\\_______\/\\\_______/\\\\\\_____   
                    _\/\\\_______\/\\\_____/\\\////\\\___  
                    _\/\\\_______\/\\\___/\\\/___\///\\\_ 
                    _\///________\///___\///_______\///__[/green]''','''

    ==================================================================================
    \t[red]欢迎使用本程序! 本程序仅供学习与交流,由于不当操作产生的问题,责任自负![/red]
    ==================================================================================

    * --> [1]. [green]查重[/green]>> 匹对文件.(看是否出现重复弹幕,有则删除)

    * --> [2]. [green]修正[/green]>> 将弹幕文件修正为可识别的样子.(可选择是否适配其他视频)

    * --> [3]. [green]合并[/green]>> 将俩个弹幕文件合并为一个.(防重复+修正)

    * --> [-1].[red]关于>> (从使用开始时,即代表同意!)[/red]

    * --> [0]. [red]退出[/red]>> 退出程序...

    ==================================================================================
    \t\t\t\t作者: [yellow]Heng_Xin[/yellow]

    \t\t\t\t版本号: V 2.0.1
    ===================================================================================
    ''')
    #1.查重功能
    #2.修正弹幕 utf-8 并且所有弹幕为任意视频都可播放 生效于BiliLocal中
    #3.合并 1+2 功能全打上...
    #4.添加了颜色
    #5.重构代码!!!

def gy():
    print('''
    ===================================================================================
    [red]\t\t\t\t关\t于[/red]
    ===================================================================================
    \t\t\t\t\b\b作者: [yellow]Heng_Xin[/yellow]

    [red][!] 请勿用于商业用途,若造成不良后果，责任自负![/red]
    
    [red][!] 项目产生的文件可能只适用于 [/red][yellow]BiliLocal[/yellow]

    [!] BiLibili主页: https://space.bilibili.com/478917126

    [!] github项目: https://github.com/HengXin666/BiLiBiLi-danmu-deal-with

    [red][!] 建议不要将不是一个视频的弹幕合并在一起.[/red]

    ===================================================================================
    ''')

if __name__ == '__main__':
    search()
    while True:
        menu()
        gn_xz = xz(-1,3) #功能_选择
        if gn_xz == 1:
            find_duplicates()
            input('\n请按回车继续...')
        elif gn_xz == 2:
            revise()
            input('\n请按回车继续...')
        elif gn_xz == 0:
            print('\t正在退出...')
            exit(code=1)
        elif gn_xz == -1:
            gy()
            input('\n请按回车继续...')
        elif gn_xz == 3:
            merge()
            input('\n请按回车继续...')