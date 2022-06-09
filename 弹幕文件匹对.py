from rich import print #一个颜色库
import re
import os
import time
import threading #多线程

def merge():
    while True:
        try:
            wj_name_1 = str(input('请输入要合并的弹幕文件[ 1 ](如 "弹幕文件.xml" ):'))
            wj_name_2 = str(input('请输入要合并的弹幕文件[ 2 ](如 "弹幕文件.xml" ):'))
            if wj_name_1 == wj_name_2:
                print('【错误】:不能合并同一个文件！(文件名不能完全相同!)')
                a = 1/0
            with open(f'{wj_name_1}','r',encoding='UTF-8')as wj:
                wj_nr_1 = wj.readlines()#获取文件1每一行保存为列表 #获取文件内容
            with open(f'{wj_name_2}','r',encoding='UTF-8')as wj:
                wj_nr_2 = wj.readlines()#获取文件2每一行保存为列表 #获取文件内容
            break
        except:
            print('[red]【错误】:请输入正确的文件名 + .xml[/red]')

    re_all = re.compile(r'(<d p="\d+\.\d+,\d,\d+,\d+,\d+,\d,.+?,\d+">.+?</d>)')#匹配弹幕
    #修复BUG高级弹幕
    re_ll_gjdm_t = re.compile(r'^(\[)\d+?,')#判断是否为高级弹幕 头部
    re_ll_gjdm_w = re.compile(r'",\d(])$')#尾部
    global new_list, cf_dm_cs, bug_gjdm, new_good_list
    cf_dm_cs = 0
    new_list = [] #搞到所有符合的弹幕的列表.(不带换行符 \n )
    bug_gjdm = 0
    n = '\n'

    wj_nr_all = wj_nr_1+wj_nr_2
    #修正:
    prtime('正在[修正]文件...')
    for x in wj_nr_all:
        new_list_preliminary = re.findall(re_all,x)
        for i in new_list_preliminary:
            dm_t = re.findall(re_ll_gjdm_t,i)
            dm_w = re.findall(re_ll_gjdm_w,i)
            if '[' in dm_t and']' in dm_w:
                danmu_nr = re.sub(r'(\\")','',i)
                print(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
                bug_gjdm+=1
            else:
                danmu_nr = i
            new_list.append(danmu_nr+'\n')
    prtime('[修正]文件完成!!!')
    new_good_list = [] #最终
    def wj_cl_f(new_list,i):
        global new_good_list, cf_dm_cs, bug_gjdm
        #获取自己那份
        #向下取整直接用内建的int() # i 是份数
        dm_list = []
        prtime(f'已启动线程数: [{i+1}]\t| 处理范围:[{int(len(new_list)/g_xc)*i},{int(len(new_list)/g_xc)*(i+1)}]')
        if i == g_xc:
            for x in range(int(len(new_list)/g_xc)*i,len(new_list)):
                dm_list.append(new_list[x])
        else:
            for x in range(int(len(new_list)/g_xc)*i,int(len(new_list)/g_xc)*(i+1)):
                # print(x,wj_nr_1[x])
                dm_list.append(new_list[x])
        for x in dm_list:
            if x not in new_good_list:
                new_good_list.append(x)
            else:
                cf_dm_cs += 1
                print(f'[{cf_dm_cs}重复]:{x.rstrip(n)}')
        # for x in dm_list:
        #     new_list_preliminary = re.findall(re_all,x)
        #     for i in new_list_preliminary:
        #         dm_t = re.findall(re_ll_gjdm_t,i)
        #         dm_w = re.findall(re_ll_gjdm_w,i)
        #         if '[' in dm_t and']' in dm_w:
        #             danmu_nr = re.sub(r'(\\")','',i)+'\n'
        #             print(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
        #             bug_gjdm+=1
        #         else:
        #             danmu_nr = i+'\n'
        #         if danmu_nr not in new_list:
        #             new_list.append(danmu_nr)
        #         else:
        #             cf_dm_cs += 1
        #             print(f'【[重复] {cf_dm_cs} 】: {danmu_nr.rstrip(n)}')

    #数据交互还是有点问题.... ! 还不学习 ?一下!    
    threads = [] #存放线程
    print('请选择线程数: \n[1]--单线程\n[2]--双线程\n[3]--四线程\n[4]--八线程\n[5]--十六线程\n[6]--三十二线程\n')
    g_xc = 2**(xz(1,10)-1)
    if len(new_list) >= g_xc:
        pass
    else:
        g_xc = len(new_list)
        print('弹幕数过少?请修复?已给您选用 {g_xc}线程...')
    
    for i in range(g_xc):#封装g_xc个线程
        threads.append(threading.Thread(target=wj_cl_f ,args=(new_list ,i)))
    prtime('封装线程完成!\n')
    for thread in threads:#启动多线程
        thread.start()
    prtime('全部线程已启动!\n')
    for thread in threads:#等待多线程
        thread.join()
    prtime('任务完成!输出文件中...\n')

    wj = open(f'合并-{wj_name_1}-{wj_name_2}','a',encoding='utf-8')
    wj.writelines('<?xml version="1.0" encoding="UTF-8"?><i><chatserver>Heng_Xin弹幕文件工具</chatserver></i>\n')
    for i in new_good_list:
        wj.writelines(i)
        wj.flush()
    wj.close()
    print(f'输出文件[ 合并-{wj_name_1}-{wj_name_2} ]完成!共有 {len(new_good_list)} 条弹幕,企图修正 {bug_gjdm} 条高级弹幕,重复弹幕 {cf_dm_cs} 条.')
def merge1():#合并(只能两个文件这样来)
    while True:
        try:
            wj_name_1 = str(input('请输入要合并的弹幕文件[ 1 ](如 "弹幕文件.xml" ):'))
            wj_name_2 = str(input('请输入要合并的弹幕文件[ 2 ](如 "弹幕文件.xml" ):'))
            if wj_name_1 == wj_name_2:
                print('【错误】:不能合并同一个文件！(文件名不能完全相同!)')
                a = 1/0
            with open(f'{wj_name_1}','r',encoding='UTF-8')as wj:
                wj_nr_1 = wj.readlines()#获取文件1每一行保存为列表 #获取文件内容
            with open(f'{wj_name_2}','r',encoding='UTF-8')as wj:
                wj_nr_2 = wj.readlines()#获取文件2每一行保存为列表 #获取文件内容
            break
        except:
            print('[red]【错误】:请输入正确的文件名 + .xml[/red]')
    
    re_all = re.compile(r'(<d p="\d+\.\d+,\d,\d+,\d+,\d+,\d,.+?,\d+">.+?</d>)')#匹配弹幕
    #修复BUG高级弹幕
    re_ll_gjdm_t = re.compile(r'^(\[)\d+?,')#判断是否为高级弹幕 头部
    re_ll_gjdm_w = re.compile(r'",\d(])$')#尾部
    bug_gjdm = 0
    cf_dm_sl = 0
    new_list = [] #搞到所有符合的弹幕的列表.(不带换行符 \n )
    # total = 0
    print(f'正在处理文件 [ {wj_name_1} ]')
    for x in wj_nr_1:
        new_list_preliminary = re.findall(re_all,x)
        for i in new_list_preliminary:
            dm_t = re.findall(re_ll_gjdm_t,i)
            dm_w = re.findall(re_ll_gjdm_w,i)
            if '[' in dm_t and']' in dm_w:
                danmu_nr = re.sub(r'(\\")','',i)
                print(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
                bug_gjdm+=1
            else:
                danmu_nr = i
            if i not in new_list:
                new_list.append(danmu_nr+'\n')
            else:
                cf_dm_sl += 1
                print('[重复]:输出了第 {cf_dm_sl} 条重复弹幕: {i}')
            # total += 1
            # if total%10000 == 0:
            #     print(f'[{time.strftime("%H:%M:%S")}]:当前已经处理弹幕: {total} 条!')
    print(f'正在处理文件 [ {wj_name_2} ]')
    for x in wj_nr_2:
        new_list_preliminary = re.findall(re_all,x)
        for i in new_list_preliminary:
            dm_t = re.findall(re_ll_gjdm_t,i)
            dm_w = re.findall(re_ll_gjdm_w,i)
            if '[' in dm_t and']' in dm_w:
                danmu_nr = re.sub(r'(\\")','',i)
                print(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
                bug_gjdm+=1
            else:
                danmu_nr = i
            if i not in new_list:
                new_list.append(danmu_nr+'\n')
            else:
                cf_dm_sl += 1
                print('[重复]:输出了第 {cf_dm_sl} 条重复弹幕: {i}')
            # total += 1
            # if total%10000 == 0:
                # print(f'[{time.strftime("%H:%M:%S")}]:当前已经处理弹幕: {total} 条!')
    
    print(f'合并完毕,正在输出文件[ 合并-{wj_name_1}-{wj_name_2} ]')
    wj = open(f'合并-{wj_name_1}-{wj_name_2}','w',encoding='utf-8')
    wj.writelines('<?xml version="1.0" encoding="UTF-8"?><i><chatserver>Heng_Xin弹幕文件工具</chatserver></i>\n')
    for i in new_list:
        wj.writelines(i)
    wj.close()
    print(f'输出文件[ 合并-{wj_name_1}-{wj_name_2} ]完成!\n共有 {len(new_list)} 条弹幕,\n企图修正 {bug_gjdm} 条高级弹幕\n重复弹幕 {cf_dm_sl} 条.')


def revise():#修正
    while True:
        try:
            wj_name = str(input('请输入要修正的弹幕文件(如 "弹幕文件.xml" ):'))
            with open(f'{wj_name}','r',encoding='UTF-8')as wj:
                wj_nr = wj.readlines()#获取文件每一行保存为列表 #获取文件内容
            break
        except:
            print('【错误】:请输入正确的文件名 + .xml')
    #匹配弹幕的正则表达式
    re_all = re.compile(r'(<d p="\d+\.\d+,\d,\d+,\d+,\d+,\d,.+?,\d+">.+?</d>)')#匹配弹幕
    #修复BUG高级弹幕
    re_ll_gjdm_t = re.compile(r'^(\[)\d+?,')#判断是否为高级弹幕 头部
    re_ll_gjdm_w = re.compile(r'",\d(])$')#尾部
    bug_gjdm = 0
    new_list = [] #搞到所有符合的弹幕的列表.(不带换行符 \n )
    for x in wj_nr:
        new_list_preliminary = re.findall(re_all,x)
        for i in new_list_preliminary:
            dm_t = re.findall(re_ll_gjdm_t,i)
            dm_w = re.findall(re_ll_gjdm_w,i)
            if '[' in dm_t and']' in dm_w:
                danmu_nr = re.sub(r'(\\")','',i)
                print(f'发现第{bug_gjdm}条异常高级弹幕,企图修正!{i}')
                bug_gjdm+=1
            else:
                danmu_nr = i
            new_list.append(danmu_nr+'\n')
    
    print(f'修正完毕,正在输出新文件: [ 修正-{wj_name} ] , 共 {len(new_list)} 条弹幕')
    wj = open(f'修正-{wj_name}','w',encoding='utf-8')
    wj.writelines('<?xml version="1.0" encoding="UTF-8"?><i><chatserver>Heng_Xin弹幕文件工具</chatserver></i>\n')
    for i in new_list:
        wj.writelines(i)
    wj.close()
    print(f'输出文件[ 修正-{wj_name} ]完成!共有 {len(new_list)} 条弹幕,企图修正 {bug_gjdm} 条高级弹幕.')

def find_duplicates():#查重
    while True:
        try:
            wj_name = str(input('请输入要查重的弹幕文件(如 "弹幕文件.xml" ):'))
            with open(f'{wj_name}','r',encoding='UTF-8')as wj:
                wj_nr = wj.readlines()#弹幕文件是从头开始的awa #获取文件内容
            break
        except:
            print('[red]【错误】:请输入正确的文件名 + .xml[/red]')

    new_list = [] #初始化列表
    reomve_list = []
    n = "\n"
    for x in wj_nr:
        if x not in new_list:
            new_list.append(x)
        else:
            reomve_list.append(x)
            print(f'[red][重复]({len(reomve_list)}条): {x.rstrip(n)}[/red]')
    
    if len(reomve_list) == 0:
        print('本文件没有重复弹幕!!!')
    else:
        print(f'匹对完毕,输出新文件: [ 无重复-{wj_name} ]')
        wj = open(f'无重复-{wj_name}','w',encoding='utf-8')
        for i in new_list:
            wj.writelines(i)
        wj.close()
        print(f'输出文件[ 无重复-{wj_name} ]完成! 原来有 {len(wj_nr)} 条弹幕 | [当前]:{len(new_list)} | [删除]:{len(reomve_list)}')

def prtime(say):
    print(f'[{time.strftime("%H:%M:%S")}]:{say}')

def search():#初始化工作区
    re_ll_wj = re.compile(r'^(.:\\)')
    dq = os.getcwd()
    print("当前工作目录 : %s" % dq)
    print('若不是您想要的工作目录,请在 [red]本盘工作目录区域[/red] 创建一个"[yellow]定位文件_请勿删除_HX001[/yellow]"文件用于定位. ')
    path = re.findall(re_ll_wj,dq)[0]
    name = '定位文件_请勿删除_HX001' #填写文件名
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

    * --> [2]. [green]修正[/green]>> 将弹幕文件修正为可识别的样子.(重新布局弹幕|弹幕文件可用于任意视频)

    * --> [3]. [green]合并[/green]>> 将俩个弹幕文件合并为一个.(防重复)(+修正)

    * --> [-1].[red]关于>> (从使用开始时,即代表同意!)[/red]

    * --> [0]. [red]退出[/red]>> 退出程序...

    ==================================================================================
    \t\t\t\t作者: [yellow]Heng_Xin[/yellow]

    \t\t\t\t版本号: V 1.4.2
    ===================================================================================
    ''')
    #1.查重功能
    #2.修正弹幕 utf-8 并且所有弹幕为任意视频都可播放 生效于BiliLocal中
    #3.合并 1+2 功能全打上...
    #4.添加了颜色

def gy():
    print('''
    ===================================================================================
    [red]\t\t\t\t关\t于[/red]
    ===================================================================================
    \t\t\t\t\b\b作者: [yellow]Heng_Xin[/yellow]

    [red][!] 请勿用于商业用途,若造成不良后果，责任自负![/red]
    
    [red][!] 项目产生的文件可能只适用于 [/red][yellow]BiliLocal[/yellow]

    [?] 代码写得很烂? 没有使用多线程等 某些时候效率可能很低? 请见谅qwq..

    [!] BiLibili主页: https://space.bilibili.com/478917126

    [!] github项目: https://github.com/HengXin666/BiLiBiLi-danmu-deal-with

    [!] 建议不要将不是一个视频的弹幕合并在一起.

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