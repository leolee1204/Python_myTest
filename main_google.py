import requests as re
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time, random, warnings
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud  #conda install -c conda-forge wordcloud
import jieba
import numpy as np
from collections import Counter
from datetime import datetime
from elasticsearch import Elasticsearch #pip install "elasticsearch<7.14"
from cra_google_map import *


#============================瓦城爬蟲===================================

# google_spider('瓦城集團_google//1010湘分店資料//1010湘_google.txt')
# google_spider('瓦城集團_google//大心分店資料//大心_google.txt')
# google_spider('瓦城集團_google//時時香分店資料//時時香_google.txt')
# google_spider('瓦城集團_google//瓦城分店資料//Thaitown_google.txt')
# google_spider('瓦城集團_google//非常泰分店資料//VeryThai_google.txt')

# merge_all_branch('瓦城集團_google//1010湘分店資料//1010湘_google', 14)
# merge_all_branch('瓦城集團_google//大心分店資料//大心_google', 33)
# merge_all_branch('瓦城集團_google//時時香分店資料//時時香_google', 14)
# merge_all_branch('瓦城集團_google//瓦城分店資料//Thaitown_google', 62)
# merge_all_branch('瓦城集團_google//非常泰分店資料//VeryThai_google', 6)

# divide_by_star('瓦城集團_google//Thaitown_google_final.json')
# divide_by_star('瓦城集團_google//1010湘_google_final.json')
# divide_by_star('瓦城集團_google//VeryThai_google_final.json')
# divide_by_star('瓦城集團_google//大心_google_final.json')
# divide_by_star('瓦城集團_google//時時香_google_final.json')


#============================王品爬蟲===================================

# google_spider('王品集團_google//石二鍋分店資料//12hotpot_google.txt')
# google_spider('王品集團_google//陶板屋分店資料//tokiya_google.txt')
# google_spider('王品集團_google//西堤分店資料//Tasty_google.txt')
# google_spider('王品集團_google//王品分店資料//wangsteak_google.txt')

# merge_all_branch('王品集團_google//石二鍋分店資料//12hotpot_google', 74)
# merge_all_branch('王品集團_google//陶板屋分店資料//tokiya_google', 35)
# merge_all_branch('王品集團_google//西堤分店資料//Tasty_google', 38)
# merge_all_branch('王品集團_google//王品分店資料//wangsteak_google', 11)

# divide_by_star('王品集團_google//石二鍋分店資料//12hotpot_google_final.json')
# divide_by_star('王品集團_google//陶板屋分店資料//tokiya_google_final.json')
# divide_by_star('王品集團_google//西堤分店資料//Tasty_google_final.json')
# divide_by_star('王品集團_google//王品分店資料//wangsteak_google_final.json')

#============================寫入SQL===================================

# write_into_sql('王品','陶板屋','王品集團_google//tokiya_google_final.json')
write_into_sql('王品','石二鍋','王品集團_google//12hotpot_google_final.json')
# write_into_sql('王品','西堤','王品集團_google//Tasty_google_final.json')
# write_into_sql('王品','王品','王品集團_google//wangsteak_google_final.json')

# write_into_sql('瓦城','瓦城','瓦城集團_google//Thaitown_google_final.json')
# write_into_sql('瓦城','1010湘','瓦城集團_google//1010湘_google_final.json')
# write_into_sql('瓦城','非常泰','瓦城集團_google//VeryThai_google_final.json')
# write_into_sql('瓦城','大心','瓦城集團_google//大心_google_final.json')
# write_into_sql('瓦城','時時香','瓦城集團_google//時時香_google_final.json')

#============================文字雲===================================

# wordcloud_result('瓦城集團_google//Thaitown_google_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//Thaitown_google_good_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//Thaitown_google_bad_final.json', 'elep-worldcloud-small.png')
#
# wordcloud_result('瓦城集團_google//1010湘_google_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//1010湘_google_good_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//1010湘_google_bad_final.json', 'elep-worldcloud-small.png')
#
# wordcloud_result('瓦城集團_google//大心_google_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//大心_google_good_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//大心_google_bad_final.json', 'elep-worldcloud-small.png')
#
# wordcloud_result('瓦城集團_google//VeryThai_google_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//VeryThai_google_good_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//VeryThai_google_bad_final.json', 'elep-worldcloud-small.png')
#
# wordcloud_result('瓦城集團_google//時時香_google_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//時時香_google_good_final.json', 'elep-worldcloud-small.png')
# wordcloud_result('瓦城集團_google//時時香_google_bad_final.json', 'elep-worldcloud-small.png')

# wordcloud_result('王品集團_google//石二鍋分店資料//12hotpot_google_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//石二鍋分店資料//12hotpot_google_good_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//石二鍋分店資料//12hotpot_google_bad_final.json', 'cattle-wordcloud-small.png')

# wordcloud_result('王品集團_google//陶板屋分店資料//tokiya_google_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//陶板屋分店資料//tokiya_google_good_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//陶板屋分店資料//tokiya_google_bad_final.json', 'cattle-wordcloud-small.png')

# wordcloud_result('王品集團_google//西堤分店資料//Tasty_google_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//西堤分店資料//Tasty_google_good_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//西堤分店資料//Tasty_google_bad_final.json', 'cattle-wordcloud-small.png')

# wordcloud_result('王品集團_google//王品分店資料//wangsteak_google_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//王品分店資料//wangsteak_google_good_final.json', 'cattle-wordcloud-small.png')
# wordcloud_result('王品集團_google//王品分店資料//wangsteak_google_bad_final.json', 'cattle-wordcloud-small.png')

