from aip import AipSpeech
APP_ID = '23555304'
API_KEY = 'pkdZt0IhXgi4udsM02YrF0Bk'
SECRET_KEY = '4HMG0VVKRPBOVkSGPsZBWwAFytzxdBPL'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open("demo.pcm", 'rb') as fp:
        return fp.read()


# 识别本地文件
test1 = client.asr(get_file_content('demo.pcm'), 'pcm', 16000, {'dev_pid': 1536, })
print(test1)