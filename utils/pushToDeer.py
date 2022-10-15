import imp
from pypushdeer import PushDeer
# from setting import pushDeerKey
import sys
import datetime

def pushToIos(text):
    date = str(datetime.date.today())
    if(len(sys.argv) != 1):
        key = sys.argv[3]
    # else:
    #     key = pushDeerKey
    pushdeer = PushDeer(pushkey=key)
    if(text == 1):
        pushdeer.send_markdown("# " + date + " 填报成功", desp="**detail** 美好的一天开始啦")
    else:
        pushdeer.send_markdown("# ERROR!", desp='**detail** ' + text)