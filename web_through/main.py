#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logging import exception
import requests
import sys
import re
# from setting import username, password
from utils.pushToDeer import pushToIos
session = requests.Session()
def login(user, passwd, urlLogin='https://uis.nwpu.edu.cn/cas/login'):
    print('login start')
    # pubkeyurl = 'https://uis.nwpu.edu.cn/cas/jwt/publicKey'
    # content = session.get(pubkeyurl)
    mfaurl = 'https://uis.nwpu.edu.cn/cas/mfa/detect'
    header = {
        "Host": "uis.nwpu.edu.cn",
        "Connection": "keep-alive",
        # "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        "Origin": "https://uis.nwpu.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fecampus.nwpu.edu.cn%2F%3Fpath%3Dhttps%3A%2F%2Fecampus.nwpu.edu.cn%2Fmain.html%23%2FIndex",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
        "X-Forwarded-For": "10.68.21.220",
        # "X-Forwarded-For": "10.68.21.229",
        # "X-Originating-IP": "113.140.3.73",
        # "X-Remote-IP":"10.68.21.220",
    }
    loginData = {
        'username': user,
        'password': passwd,
    }
    text = session.post(mfaurl, data=loginData, headers=header).text
    mfastate = re.findall(',"state":"(.*?)"', text)[0]
    isNeed = re.findall('"need":(.*?),', text)[0]
    session.get(urlLogin)
    # 登录页请求头
    header = {
        'Origin': 'https://uis.nwpu.edu.cn',
        'Referer': urlLogin,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    # 登录信息
    loginData = {
        'username': user,
        'password': passwd,
        'currentMenu': 1,
        'execution': re.findall("""name="execution" value="(.*?)"/>""", session.get(urlLogin).text)[0],  # 和find哪个快
        '_eventId': 'submit',
        'mfaState': mfastate,
        'geolocation': '',
        'submit': '稍等片刻……'
    }

    res = session.post(url=urlLogin, data=loginData, headers=header).text
    if('欢迎使用' in res):
        print('login  successfully')
    elif(isNeed == 'true'):
        pushToIos('need verify')
# def login_check(user='', passwd=''):
#     print('login_check start')
#     '''
#     检查登录状态, 若登录失败则反复尝试
#     '''
#
#     session, status = login(user=user, passwd=passwd)
#     while True:
#         if status == 1:
#             print('login_check  done')
#             return session
#         else:
#             if status == -1:
#                 remove_cache()
#                 exit(-1)
#             else:
#                 print('正在重新登录...')
#                 session, status = login(user=user, passwd=passwd)
def tianbao(name):
    print('tianbao start')
    url_form = 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp'
    url_tianbao = 'https://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp'
    data_tianbao = {
        'hsjc': '1',
        'xasymt': '1',
        'actionType': 'addRbxx',
        'userLoginId': name,
        'szcsbm': '1',
        'bdzt': '1',
        'szcsmc': '在学校',
        'szcsmc1': '在学校',
        'sfyzz': '0',
        'sfqz': '0',
        'tbly': 'pc',
        'qtqksm': 'Hava a nice day~',
        'ycqksm': '',
        'sfxn': '0',
        'sfdw': '0',
        'longlat': '',
        'userType': '2',
        'userName': 'BIGBOSS',
    }
    formHeaders = {
        'Origin': 'https://yqtb.nwpu.edu.cn',
        'Referer': url_form,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    session.get(url=url_form)
    para = session.get(url=url_form).text
    sign_ = para.find('sign=')
    sign = para[sign_ + 5: sign_ + 45]
    timeStamp_ = para.find('timeStamp=')
    timeStamp = para[timeStamp_ + 10: timeStamp_ + 23]
    url_tianbao = url_tianbao + '?sign=' + sign + '&timeStamp=' + timeStamp
    r = session.post(url_tianbao, data_tianbao, headers=formHeaders)
    if (re.findall('{"state":"1"}', r.text)):
        print('tianbao successfully')
        pushToIos(1)
if __name__ == '__main__':
    if (sys.argv[1]):
        try:
            login(sys.argv[1], sys.argv[2])
            tianbao(sys.argv[1])
        except exception as e:
            pushToIos(e)
    # else:
    #     try:
    #         login(username, password)
    #         tianbao(username)
    #     except exception as e:
    #         pushToIos(e)
