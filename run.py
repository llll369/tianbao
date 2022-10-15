from web_through.main import login,tianbao
# from setting import username,password
import sys
# from app_through.NWPU import nwpuapp
if __name__ == '__main__':
    if (len(sys.argv) != 1):
        login(sys.argv[1], sys.argv[2])
        tianbao(sys.argv[1])
    # else:
    #     login(username, password)
    #     tianbao(username)

    # app = nwpuapp()
    # app.getidToken()
    # app.yqtb_one_sesstion()
