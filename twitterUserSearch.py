#!/usr/bin/env python
# coding: utf-8

# In[1]:


#TwitterAPI
import tweepy
CK = 'MOUAnEZcVXbuymSvEq4GSPCqR' #consumer_key
CS = 'kGcCpaKTTh5W3bR3f05gzpemhsbMmoTKvYvoYPSptAq4Dwnn8r' #consumer_secret
AT = '1254808886667665409-doIXOMOrC1shBHUQUz5dHCvgQ0z9Nc' #Access_token
AS = 'Vtjq1jEtsE4BUgv07aAquUUVhSh3bYNlUi4ISiBh6vEYz' #Access_token_secret
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

#インスタンス作成
twitter_api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
#print(twitter_api.me)
screen_name = 'apricot_ship05' #@はいらない
search_result = twitter_api.get_user(screen_name)
print(search_result)
f = open('twitterUserSearchResult.txt', 'a', encoding="UTF-8") #第二引数がw:上書き書き込み a:追加書き込み x:ファイルがあったらエラーを吐く　全ての引数でファイルがなかったら作成する
f.writelines(search_result)
f.close()

