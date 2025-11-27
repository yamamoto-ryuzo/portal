# .envサンプル（APIキー例）
# ----------------------------------
# TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxxx
# TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# TWITTER_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# TWITTER_ACCESS_TOKEN_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# TWITTER_BEARER_TOKEN=ここに取得したBearer Tokenを貼り付けてください
# ※このうち本スクリプトで必要なのはTWITTER_BEARER_TOKENのみです

# Twitterデータ収集用スクリプト（サンプル）
# 必要なライブラリ: tweepy
# pip install tweepy
# pip install python-dotenv

import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

# Bearer Token（API v2用）を環境変数から取得
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
if not BEARER_TOKEN:
    raise ValueError('Twitter API v2用のBEARER_TOKENが環境変数に設定されていません。')

# tweepy.Clientで認証
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# 収集したいキーワードやハッシュタグ
SEARCH_QUERY = '#地域課題 OR #市民意見 OR #渋谷'

# 収集件数
MAX_TWEETS = 100

# データ収集

# v2 API用のデータ収集関数
def collect_tweets_v2(query, max_count=100):
    tweets_data = []
    # 位置情報取得のためのフィールド指定
    response = client.search_recent_tweets(
        query=query,
        max_results=min(max_count,100),
        tweet_fields=['created_at','text','author_id','lang','geo'],
        expansions=['geo.place_id'],
        place_fields=['full_name','country','geo']
    )
    # place_idとplace情報の紐付け
    places = {}
    if response.includes and 'places' in response.includes:
        for p in response.includes['places']:
            places[p.id] = p
    if response.data:
        for t in response.data:
            place_info = None
            if t.geo and 'place_id' in t.geo:
                place_obj = places.get(t.geo['place_id'])
                if place_obj:
                    place_info = {
                        'full_name': place_obj.full_name,
                        'country': place_obj.country,
                        'geo': getattr(place_obj, 'geo', None)
                    }
            tweets_data.append({
                'id': t.id,
                'author_id': t.author_id,
                'created_at': t.created_at,
                'text': t.text,
                'place': place_info
            })
    return tweets_data

if __name__ == '__main__':
    tweets = collect_tweets_v2(SEARCH_QUERY, MAX_TWEETS)
    for t in tweets:
        print(f"[{t['created_at']}] @{t['author_id']}: {t['text']}")
        if t['place']:
            print(f"  位置情報: {t['place']['full_name']} ({t['place']['country']})")

## ...existing code...
