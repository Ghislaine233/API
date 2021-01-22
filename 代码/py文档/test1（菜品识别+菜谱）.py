import requests
from lxml import etree
from urllib.parse import urljoin,quote
import requests,base64
#百度api
from os import system
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=nU2uq3B8rmkxhETkReNwlC07&client_secret=OeTRkbpS7Bf8SxYZE9MkGTv4I3gtOcDd'
response = requests.get(host)
#if response:
#    print(response.json())
#使用百度ai识别菜品
request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/dish'
#打开图片所在位置
f = open('../pic/food.jpg','rb')
img = base64.b64encode(f.read())

params = {
    "image":img,
    "top_num":5
}

access_token = '24.14339a91fe46c936c7dc5eb7ebb741c9.2592000.1611538484.282335-23393754'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type':'application/x-www-form-urlencoded'}
response = requests.post(request_url,data=params,headers=headers)

#if response:
#    print(response.json())

df = response.json()['result'][0]["name"]
print("这道菜的名字是"+df)

print("----------------以下是做法-----------------")

#爬虫返回菜谱
BASE_URL = "https://www.xinshipu.com/"
#使用菜品识别的结果
name = df
#name = input("请输入菜名：")
url = f"https://www.xinshipu.com/doSearch.html?q={quote(name)}"

headers = {
  'Authorization': 'admin eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJndWVzdCIsImV4cCI6MTYwNDY2NTI0MX0.dUAgnQFNBmO7lf5RtgNQYOvmrp-fzbpkLLZUqz_tQEdjbDDdCuT7BTV0pbS3bcdx-pDfbfpksz7Zid2IAfFJW5mapAael_J2aVZrCO7gIWOUXaWfmEmzhG0vtgSRpZa8xyy77nMVl72M3ynNAUwe25SSEM416xoOIh6c3kMJiKdkZ-oZmouDxsIfTowki4SA3TK1afVzaWq_gHyv3DbsUDV4rCvcxm359oR2xFy1xHR0OVrqv_0ExXFV0unDtLfWX4zIbQqNM9JHlKE8NTUeLfHfnY6F8C9qeEBnF0bkrigQvsOBt-TihghAFs3YF53mujE8XB7L0eiqIo-CianPztkYdjuE-W0IwddeHxOSUqKZ0C1rmhg6jSmYX7E5Y5oGeValuLKHNOhy7VlwL8vrmQOi5kH9TKYIyHT5u0u_H5R04rqccIxcdk1ghDSPvl6vMVyDTV2vxUmg8GKCcPqDjJ-giyE4rr58zJJ2fH8RXfVLHy5CokaZ67gcjNYBXf9CoXkmEJwihrxM5TPz-fS950gLQ5M2hWx1X2v8FNoLD5_v9iIvOyQuIT1PrfLFGvuxEwXXGtPaaJ9gEOEwA9QsQqruOycKArBFGVF7rclyUdfts_01TskcKvaTXVZGcT_jeDYzoDkB_Rjq3GQSLTAtopW5MOnPG4oYyz1uJ-w7Klo',
  'Cookie': 'session=eyJ0b2tlbiI6IjMyMjE6TUVRQ0lFUWtLdS9VYStpUWRyaTQ2ZnBLWVFleVNZUm9rdVl4WFN1WFAxazBDa1RJQWlCbDVwMVhrKzdObDdBdUYrRDF0WnRKYzB5eXZYMWM4aGNRejVDMEJiQ2xJQT09In0.X6U1og.0uZAuAx2LFQrka8jUvlwOHM7F7g; JSESSIONID=F80F30BED002D6A35127AE8FEF9612F2'
}

response = requests.get(url, headers=headers, allow_redirects=False)
next_url = urljoin(BASE_URL,response.headers['location'])
response = requests.get(next_url, headers=headers)
soup = etree.HTML(response.text)
# print(next_url)
div_list = soup.xpath('//ul[@class="search-list mt-12 clearfix"]/li')
for div in div_list:
  try:
    href = div.xpath('a/@href')[0]
    innerUrl = urljoin(BASE_URL,href)
    title = div.xpath('a/div/div/p/text()')[0]
    img_src = div.xpath('a/div/img/@src')[0]
    img = urljoin(BASE_URL,img_src)

    # 以下是做法
    response = requests.get(innerUrl,headers=headers)
    zuofa_soup = etree.HTML(response.text)
    zuofa = "".join(zuofa_soup.xpath('//div[@class="swipeboxEx mlr1 bbm"]//text()')).strip()
    print(zuofa)
  except:
    print("出错啦")