import pandas as pd
from selenium import webdriver
from time import sleep
import random
from bs4 import BeautifulSoup
import json
import seaborn as sns
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import pyautogui
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler  #pip install APScheduler

def login(name):
    Account = input('input Account: ')
    Password = input('input Password: )
    global driver
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(f"https://www.instagram.com/explore/tags/{name}/")
    sleep(random.randint(4, 6))
    # 登入葉面
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
        sleep(random.randint(2, 4))
    except:
        pass
    finally:
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(Account)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(Password)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
        sleep(random.randint(3, 6))
        # 登入葉面
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        sleep(random.randint(4, 7))

def scroll_page(name,year):
    #無限滾動
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    linkList = []
    #記數量
    count = 0
    herfdic = {}
    while True:
        #循环将滚动条下拉
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(random.randint(3,5))
        #擷取連結資訊
        soup = BeautifulSoup(driver.page_source,'lxml')
        hreflink = "https://www.instagram.com" + soup.select("div.Nnq7C.weEfm > div.v1Nh3.kIKUG._bz0w > a")[-1].get('href')
        #開新分頁
        pyautogui.hotkey('ctrl', 't', interval=0.1)
        driver.switch_to.window(driver.window_handles[1])
        driver.get(hreflink)
        # herfdic[hreflink] = herfdic.get(hreflink,0) + 1
        sleep(random.randint(3,5))
        #篩選日期
        soup2 = BeautifulSoup(driver.page_source, 'lxml')
        date = soup2.select_one('time._1o9PC').text
        herfdic[hreflink] = herfdic.get(hreflink,0) + 1
        # 2020年重複3次
        if count > 3:
            break
        elif year in date:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            links = soup.select('div.v1Nh3.kIKUG._bz0w > a')
            for link in links:
                linkList.append("https://www.instagram.com" + link.get("href"))
            count += 1
        #日期未到 但頁面以至底大於2次就break
        elif herfdic[hreflink] > 2:
            break
        else:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            links = soup.select('div.v1Nh3.kIKUG._bz0w > a')
            for link in links:
                linkList.append("https://www.instagram.com" + link.get("href"))
            #获取当前滚动条距离顶部的距离
            newHeight = driver.execute_script("return document.body.scrollHeight")
            #如果两者相等说明到底了
            if newHeight == lastHeight:
                driver.find_element_by_css_selector("div.Nnq7C.weEfm:last-child > div.v1Nh3.kIKUG._bz0w:last-child > a").click()
                sleep(random.randint(1,3))
                driver.find_element_by_xpath('/html/body/div[6]/div[1]/button').click()
                sleep(random.randint(1, 3))
            lastHeight = newHeight
            count = 0

    pagelist = list(set(linkList))
    with open(name + "ig_link.json","w")as f:
        json.dump(pagelist,f)
    return pagelist

def getContent(pagelist,name):
    datelist = []
    contentlist = []
    for link in pagelist:
        driver.get(link)
        sleep(random.randint(3, 5))
        soup = BeautifulSoup(driver.page_source,'lxml')
        contents = soup.find("div",class_="MOdxS")
        try:
            for content in contents:
                contentlist.append(content.text.strip())
        except Exception as e:
            print(e)
            continue
        date = soup.select_one("time._1o9PC").get("datetime").split("T")[0][:-3]
        datelist.append(date)
    with open (name + "date.json","w",encoding="utf-8")as f:
        json.dump(datelist,f)
    with open (name + "content.json","w",encoding="utf-8")as f:
        json.dump(contentlist,f,ensure_ascii=False)
    driver.quit()

def getDatePic(name,year):
    dic = {}
    for row in json.load(open(name+"date.json","r",encoding="utf-8")):
        dic[row] = dic.get(row,0)+1

    df = pd.DataFrame(dic.values(),index=dic.keys(),columns=["counts"])
    #轉化成時間 只取年分與月份
    df.index = pd.to_datetime(df.index, format="%Y-%m")
    df.sort_index(ascending=False,inplace=True)
    df_twoyear = df[(df.index >= f'{str(int(year.replace("年",""))+1)}-01')]

    df_twoyear.index = df_twoyear.index.astype(str)
    #只取到月份不要日
    result = [row[:7] for row in df_twoyear.index]

    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.figure(figsize=(12,10))
    plt.title("IG 會員發文數",fontsize=30)
    plt.xlabel("xlabel",fontsize=20)
    plt.ylabel("ylabel", fontsize=20)
    sns.barplot(x=result, y=df_twoyear["counts"])
    plt.savefig(name + "日期統計")

def wordCloudContent(name):
    wordlist = []
    for x in json.load(open(name + 'content.json',"r", encoding="utf-8")):
        wordlist.append(x.split("#")[0])

    newwordlist = [word for word in wordlist if word != '']
    jiebalist = jieba.cut("".join(newwordlist))
    jiebaword = " ".join(jiebalist)

    stopwords = set()
    content = [stopword.strip() for stopword in open("stopword.txt", "r", encoding="utf-8").readlines()]
    stopwords.update(content)

    font_path = "C:\\Windows\\Fonts\\kaiu.ttf"

    if name in ["石二鍋", "王品牛排", "西堤牛排","夏慕尼"]:
        imgname = "cow.png"
    elif name in ['瓦城', '非常泰', '1010湘', '時時香']:
        imgname = "elep.png"

    maskPic = np.array(Image.open(imgname))
    plt.figure(figsize=(12,10))
    wc = WordCloud(background_color="white", stopwords=stopwords, mask=maskPic, font_path=font_path).generate(jiebaword)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(name+"文字雲.png")

def writefinJson(name):
    datalist = []
    with open(name + 'date.json','r',encoding='utf-8')as f:
        dates = (json.load(f))
    with open(name + 'content.json','r',encoding='utf-8')as f:
        contents = (json.load(f))
    for date,content in zip(dates,contents):
        dic = {}
        #改成2021-MM-ddTHH:mm:ss
        dic["date"] = datetime.strptime(date, "%Y-%m").isoformat()
        dic["content"] = content
        datalist.append(dic)

    with open(name + '.json','w',encoding='utf-8')as f:
        f.write(json.dumps(datalist,ensure_ascii=False))

def my_function():
    #透過python排程，此段可拉掉，改為linux crontab進行排程
    year = '2020年'
    names = ["石二鍋", "王品牛排", "西堤牛排", "夏慕尼", '瓦城', '非常泰', '1010湘', '時時香']

    for name in names:
        login(name)
        pagelist = scroll_page(name,year)
        getContent(pagelist, name)
        getDatePic(name, year)
        wordCloudContent(name)
        writefinJson(name)

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(my_function, 'cron', day_of_week='mon-fri', hour=23, minute=30, end_date='2023-01-01') #每周1-5 23:30開始 到2023年1月1日
    sched.start()
