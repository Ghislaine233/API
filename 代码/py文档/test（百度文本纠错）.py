from aip import AipFace,AipBodyAnalysis
from IPython.display import Image
from IPython.core.display import HTML
from aip import AipNlp
""" 你的 APPID AK SK """
APP_ID = '23575550'
API_KEY = 'fr8nHvzt2FtHfvOLeaen7uju'
SECRET_KEY = 'Mrfk2PZR2z4AtNWFzDhCvz7AQxNrps0e'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
text = "驴打滚，是东北地区、老北京和天津卫传通小吃之一，因其最后制作工序中撒上的黄豆面，犹如老北京郊外野驴撒欢打滚时扬起的阵阵黄土，因此而得名“驴打滚”。"

""" 调用文本纠错接口 """
print(client.ecnet(text))