# -*- coding:utf-8 -*-

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": "aisjiuxu", "tte": "utf8",
                             "ent": "aisound"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
     # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:

            with open('./xunfei_audio.pcm', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./xunfei_audio.pcm'):
            os.remove('./xunfei_audio.pcm')

    thread.start_new_thread(run, ())

if __name__ == "__main__":
   #信息填写
    wsParam = Ws_Param(APPID='5fe5c149', APIKey='dd7fafbd9c3466de86e7d005b49d59fd',
                       APISecret="f4fa7e0c3cac5fde4276d376157d7733",
                       Text="他的世界是平凡的，这只是黄土高原上几千几万座村落中的一座。从小处着眼，作者刻画出一个个普通人物平凡的人生旅程，衬托日新月异的时代变迁，反映人们的思想，给人以亲近，给人以启迪。但路遥却在平凡中看到了他的主人公的不平凡。比如说孙少平，我认为孙少平这个人物是全篇文字的主线，通过他的成长和成熟的经历，展现给大家面前的是那个时代整整一代人对生活的憧憬与无奈。他受过了高中教育，他经过自学达到可与大学生进行思想探讨的程度。作者赋予了这个人物各种优良的品质，包括并不好高骛远。贫穷曾让许多有理想的人们意志消亡，可在逆境中人们的自卑与懦弱我们没有理由去嘲笑它，相反我们要用另外一种眼光去学会欣赏。那种战胜自我，重塑信心的渴望中所表现出自卑里的坚强让我敬畏，因为那也是一种精神。战胜困难，摆脱束缚，让人们对美好生活的向往，如何的体会生活中间的亲情、友情、爱情，学会生活，懂得珍惜，对于我们这一代人，也是一种警醒。在路遥的世界中出现的都是平凡的人物，正是在这些平凡的人物里他描写着人性中的善与美，丑与恶。在他的世界里，人的最大的优点就是认识到自己是平凡的。")
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})