import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from datetime import datetime
import json

def ptt(brand):
    pttlinks = []
    session = requests.Session()
    #因ptt有大於18歲的條件，先送一個post過去網站
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    session.post('https://www.ptt.cc/ask/over18', data=payload)

    i = 1
    while True:
        print(f"正在尋找第{i}頁")
        sleep(random.randint(2,6))
        url = f'https://www.ptt.cc/bbs/Gossiping/search?page={i}&q={brand}'
        res = session.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')
            titles = soup.select('div.title > a')
            for title in titles:
                pttlinks.append('https://www.ptt.cc' + title.get('href'))
            i+=1
        else:
            break

    return pttlinks

def get_content(pptlinks,brand):
    datalist = []
    session = requests.Session()
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    session.post('https://www.ptt.cc/ask/over18', data=payload)
    header = {
        'user-agent': 'input yours user-agent'
    }
    print("內容處理中...")
    for link in pptlinks:
        res = session.get(link,headers=header)
        soup = BeautifulSoup(res.text,'lxml')
        year = soup.find_all('span',class_='article-meta-value')[-1].text[-4:]
        contents = soup.find_all('span',class_='f3 push-content')
        times = soup.find_all('span',class_='push-ipdatetime')
        
        for t,c in zip(times,contents):
            dic = {}
            time = re.findall(r'.+(\d{2}/\d{2}).+',t.text.strip())
            if time != []:
                dic['time'] = year + '/' + str(time[0])
                dic['content'] = c.text
                datalist.append(dic)
    with open(brand + ".json", "a", encoding="utf-8") as fon:        
        fon.write(json.dumps(datalist,ensure_ascii=False))
    print("時間格式轉換中...")
    # "2022/05/17"
    for i in datalist:
        i['time'] = i['time'].replace('/', "-")
        i['time'] = datetime.strptime(i['time'], "%Y-%m-%d").isoformat()

    # output_ = filename.replace('result','final')
    tmp = json.dumps(datalist, ensure_ascii=False)
    # result = tmp.strip('[]')
    with open(brand + "_ptt.json", 'w', encoding="utf-8") as f:
        f.write(tmp)
if __name__ == "__main__":
  brand = input("請輸入在八卦版搜尋的關鍵字：")
  pptlinks = ptt(brand)
  get_content(pptlinks,brand)
