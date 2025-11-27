# 市民発信データ収集システムにおけるTwitterデータとAPI使用例

## 利用目的

市民発信データ収集システムでは、Twitter上の市民の声や意見をリアルタイムに収集・分析し、都市政策の検討や地域課題の把握、市民参加促進に活用します。

## 取得・活用するTwitterデータ
- ツイート本文（市民の意見・課題・提案）
- 投稿日時
- ユーザー名（匿名化処理）
- 位置情報（地域課題の空間分析）
- ハッシュタグ（#地域課題 など）
- 画像・動画（必要に応じて）

## API使用例

### 1. 市民意見・課題の収集
```python
for tweet in api.search_tweets(q="#地域課題 OR #市民意見", lang="ja", count=100):
    print(tweet.text)
```

### 2. 地域ごとの課題抽出（位置情報付き）
```python
for tweet in api.search_tweets(q="#渋谷", geocode="35.6581,139.7017,1km", count=50):
    print(tweet.text, tweet.coordinates)
```

### 3. リアルタイムで市民の声を収集
```python
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

stream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
stream.filter(track=["#市民参加", "#地域課題"], languages=["ja"])
```

### 4. 市民参加状況の可視化（ユーザー情報取得）
```python
user = api.get_user(screen_name="TwitterJP")
print(user.name, user.followers_count)
```

### 5. 市民発信データのフィードバック（投稿例）
```python
api.update_status("市民の声をもとに施策を検討中 #市民参加")
```

---

これらのAPIを活用し、収集したTwitterデータをAI分析・可視化・フィードバックすることで、地域課題の抽出や市民参加型まちづくりを推進します。
