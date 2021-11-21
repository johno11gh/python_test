#!/usr/bin/env python
# coding: utf-8

# In[1]:


#TwitterAPI
import tweepy
CK = '' #consumer_key
CS = '' #consumer_secret
AT = '-' #Access_token
AS = '' #Access_token_secret
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

