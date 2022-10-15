

from urllib import response

import requests
import json
import re
from setting import password,username,device_id
class nwpuapp(object):
    def __init__(self) -> None:
        self.session = requests.Session()
        self.device_id = device_id
        self.username = username
        self.password = password

    def getidToken(self):
        mfa_url = 'https://token.nwpu.edu.cn/mfa/detect'
        header = {
            "Host": "token.nwpu.edu.cn",
            "X-Device-Infos": "packagename=com.supwisdom.nwpuSuperapp;version=1.1.8;system=iOS",
            "User-Agent": "SWSuperApp/1.1.8 (iPhone; iOS 15.4.1; Scale/3.00)",
        }
        data = {
            "deviceId": self.device_id,
            "password": self.password,
            "username": self.username,
        }
        res = self.session.post(url=mfa_url, headers=header, data=data).text
        j = json.loads(res)
        self.mfaState = j['data']['state']
        self.isVerify = j['data']['need']

        token_url = 'https://token.nwpu.edu.cn/password/passwordLogin'

        data2 = {
            'appId': 'com.supwisdom.nwpuSuperapp',
            'clientId': 'a4a968c1bfe71afa15fd44661ea74652',
            'deviceId': self.device_id,
            'mfaState': self.mfaState,
            'osType': 'iOS',
            'password': self.password,
            'username': self.username,
        }
        res2 = self.session.post(
            url=token_url, headers=header, data=data2).text
        j2 = json.loads(res2)
        self.idToken = j2['data']['idToken']
        print()
        print()

    def getinfo(self):
        info_url = 'https://ecampus.nwpu.edu.cn/portal-api/v1/thrid-adapter/get-person-info-card-list'
        header = {
            'Host': 'ecampus.nwpu.edu.cn',
            'X-Terminal-Info': 'app',
            'X-Device-Info': 'AppleiPhone14,53.2.8.80430',
            'X-Device-Infos': '{"packagename":__UNI__AA068AD,"version":1.1.8,"system":iOS 15.4.1}',
            'User-Agent': 'iPhone14,5(iOS/15.4.1) Uninview(Uninview/1.0.0) Weex/0.26.0 1170x2532',
            'X-Id-Token': self.idToken,
        }
        res = self.session.get(url=info_url, headers=header).text
        j = json.loads(res)
        print(j['data'][1]['amount'])

    def yqtb_one_sesstion(self):
        yqtb_begin_url = 'https://yqtb.nwpu.edu.cn/sso/login.jsp'
        header3 = {
            # 'Host': 'yqtb.nwpu.edu.cn',  很关键的一步，去掉后每次跳转均正常，即会自动根据下一跳地址确定host
            'userToken': self.idToken,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'Authorization': 'JWTToken ' + self.idToken,
            'X-Id-Token': self.idToken
        }
        response = self.session.get(
            url=yqtb_begin_url, headers=header3, allow_redirects=True)
        # response_list = response.history
        sign = re.findall('sign=(.*?)&timeStam', response.text)[0]
        timestamp = re.findall("&timeStamp=(.*?)',", response.text)[0]

        yqtb_tianbao_url = 'https://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp?sign=' + \
            sign + '&timeStamp=' + timestamp
        header6 = {
            'Host': 'yqtb.nwpu.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://yqtb.nwpu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'Referer': 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp',
        }
        data6 = {
            'hsjc': '1',
            'xasymt': '1',
            'actionType': 'addRbxx',
            'userLoginId': self.username,
            'szcsbm': '1',
            'bdzt': '1',
            'szcsmc': '在学校',
            'szcsmc1': '在学校',
            'sfyzz': '0',
            'sfqz': '0',
            'tbly': 'app',
            'qtqksm': 'Hava+a+nice+day~',
            'ycqksm': '',
            'sfxn': '0',
            'sfdw': '0',
            'longlat': '',
            'userType': 2,
            'userName': '刘嘉尧',
        }
        res6 = self.session.post(url=yqtb_tianbao_url,
                                 headers=header6, data=data6).text
        if ('{"state":"1"}' in res6):
            print('success')

    # def getTGCCookies(self):
    #     uis_url = 'https://uis.nwpu.edu.cn/cas/login?service=https%3A%2F%2Fyqtb.nwpu.edu.cn%2F%2Fsso%2Flogin.jsp%3FtargetUrl%3Dbase64aHR0cHM6Ly95cXRiLm53cHUuZWR1LmNuLy93eC94Zy95ei1tb2JpbGUvaW5kZXguanNw'
    #     header4 = {
    #         'Host': 'uis.nwpu.edu.cn',
    #         'userToken': self.idToken,
    #         'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
    #         'X-Id-Token': self.idToken
    #     }
    #     response = self.session.get(
    #         uis_url, headers=header4, allow_redirects=False)
    #     self.session.cookies.update(response.cookies)
    #     print(111)

    def yqtb_manualLocation(self):
        yqtb_begin_url = 'https://yqtb.nwpu.edu.cn/sso/login.jsp'
        header3 = {
            'Host': 'yqtb.nwpu.edu.cn',
            'userToken': self.idToken,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'Authorization': 'JWTToken ' + self.idToken,
            'X-Id-Token': self.idToken
        }
        response = self.session.get(
            url=yqtb_begin_url, headers=header3, allow_redirects=False)
        # self.session.cookies.update(response.cookies)
        # 遇到跨域请求时，需要手动跳转
        uis_url = response.headers['Location']
        header4 = {
            'Host': 'uis.nwpu.edu.cn',
            'userToken': self.idToken,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'X-Id-Token': self.idToken
        }
        response = self.session.get(
            uis_url, headers=header4, allow_redirects=False)
        # self.session.cookies.update(response.cookies)
        yqtb_url = response.headers['Location']
        header5 = {
            'Host': 'yqtb.nwpu.edu.cn',
            'userToken': self.idToken,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'X-Id-Token': self.idToken,
        }
        res5 = self.session.get(url=yqtb_url,headers=header5).text

        self.sign = re.findall('sign=(.*?)&timeStam', res5)[0]
        self.timestamp = re.findall("&timeStamp=(.*?)',", res5)[0]

        yqtb_tianbao_url = 'https://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp?sign=' + \
            self.sign + '&timeStamp=' + self.timestamp
        header6 = {
            'Host': 'yqtb.nwpu.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://yqtb.nwpu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app SuperApp-10699',
            'Referer': 'https://yqtb.nwpu.edu.cn/wx/ry/jrsb_xs.jsp',
        }
        data6 = {
            'hsjc': '1',
            'xasymt': '1',
            'actionType': 'addRbxx',
            'userLoginId': self.username,
            'szcsbm': '1',
            'bdzt': '1',
            'szcsmc': '在学校',
            'szcsmc1': '在学校',
            'sfyzz': '0',
            'sfqz': '0',
            'tbly': 'app',
            'qtqksm': 'Hava+a+nice+day~',
            'ycqksm': '',
            'sfxn': '0',
            'sfdw': '0',
            'longlat': '',
            'userType': 2,
            'userName': '刘嘉尧',
        }
        res6 = self.session.post(url=yqtb_tianbao_url,
                                 headers=header6, data=data6).text
        if ('{"state":"1"}' in res6):
            print('success')


if __name__ == '__main__':
    app = nwpuapp()
    app.getidToken()
    # app.getinfo()

    app.yqtb_one_sesstion()
    # app.yqtb_manualLocation()
