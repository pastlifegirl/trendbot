#!/usr/bin/python3
# -*- coding: utf-8 -*-
from twitter import *
import re
import sqlite3
import random
import tweepy

DB_NAME = 'trend_word.db'

# 環境に適した値を書くこと
CONSUMER_KEY = '***'
CONSUMER_SECRET = '***'
ACCESS_TOKEN = '***'
ACCESS_TOKEN_SECRET = '***'


def updateTweet(content):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit = True)
	
	api.update_status(content)

if __name__ == "__main__":
	auth = OAuth(ACCESS_TOKEN,ACCESS_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
	twitter = Twitter(auth = auth)

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()

	sql = "SELECT name FROM words"
	res = c.execute(sql)

	used = {}
	for r in res:
		used[r[0]] = True

	# 23424856 : 日本のトレンド番号
	pid = 23424856
	mode = 0

	results = twitter.trends.place(_id = pid)
	list_trend = []
	for result in results:
		for trend in result['trends']:
			# ハッシュタグの#は取り除いている
			trend['name'] = re.sub('^#','', trend['name'])
			list_trend.append(trend['name'])

	sql = ""
	for trend in list_trend:
		if not trend in used:
			sql = 'INSERT INTO words VALUES(\"' + trend + '\")' 
			# ここは好きに変えれば良い
			print(trend + "から逃げるなぺらい丸")
			updateTweet(trend + "から逃げるなぺらい丸")
			break

	c.execute(sql)
	conn.commit()
	conn.close()
