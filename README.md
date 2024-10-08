# TwitterBot

🦉 A telegram Twitter bot that will allow you to send tweets!

Supports Twitter API v2! 🎉🎉🎉🎉🎉🎉

# Features

All the following features rely on authorized users.

* send text tweet
* send tweet with one photo(photo and document are supported.)
* reply bot tweet message to add more tweets to this thread
* reply `/delete` to delete tweet
* ~~send any video tweet to download the video~~ If you have Basic or Access subscription, you can download video tweet.
* send pictures as media group, it will result in multiple photos in your tweet(max photo restrictions is 4)

# Commands

```
start - Start using it today
sign_in - Go to sign in with Twitter
sign_off - sign off from Twitter
help - What is this bot
ping - Status about this bot
delete - Delete tweet
```

# Usage

## 长度大于130的中文tweet，将拆分为多段发送，且第二段的内容为第一段推文的回复信息。

The most simple way to tweet!

![](assets/tweet.png)

## Sign in

Chat with [this bot](https://t.me/JPTweetForwardBot), and go to oauth by its instruction:
![](assets/intro.png)

Copy and paste the auth code to this bot. And you're good to go!

## Tweet

### New thread tweet

Send any text message, photo/photo as file with caption will send tweet with photos.

![](assets/tweet_web.png)

### Reply to this thread

Reply to bot's tweet message,

![](assets/thread-bot.png)

and you'll consult in a series of thread.

![](assets/thread-web.png)

## Delete tweet

Reply command `/delete` to bot's message and it will delete this tweet for you.

![](assets/delete.png)

## Download tweet video

**ONLY WORKS IF YOU HAVE BASIC OR PRO SUBSCRIOTION**

You could just send any video tweet, such as this one

https://x.com/jp0id/

The bot will first determine if this is a video tweet, if the answer is yes,
it will ask what do you want to do with it:

![](assets/download_or_tweet.png)

Depending on your choice, this bot will download this video or retweet.

![](assets/video_choice.png)

## multiple photo mode

**Group feature requires a newer version of Telegram**
Just send a group of photos, add some captions if you want to, and hit send.
![](assets/multi_photo.jpg)

**Warning: if you send more than four photos in a group, this bot will only send first four photos in a tweet**

# General deployment

This bot use oauth, so you need to apply an app, setup callback url.

## Setup Twitter Developer

1. Apply a Twitter Developer account https://developer.twitter.com/en/portal/dashboard
2. Create a project
3. Create an app and attach it to your project. Remember API key and API secret key!
4. User authentication settings, Click Edit and enable OAuth
5. App permissions Read/Write, Web App, Automated App or Bot, Callback `http://YOUR_IP:8888/callback`

## Setup Telegram APP ID

Get it from https://core.telegram.org/

## Run Web server

```shell script
vim twauth.py
# change this three lines to your own
# CONSUMER_KEY ---> API key
# CONSUMER_SECRET ---> API secret key
APP_CONSUMER_KEY = os.environ.get("CONSUMER_KEY") or '1'
APP_CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") or '2'
callback_url = os.environ.get("CALLBACK_URL") or "http://YOUR_IP:8888/callback"

# run it
python3 twauth.py
```

Open `http://YOUR_IP:8888` in your browser and follow the instructions.

## Run Bot

```shell script
git clone https://github.com/Jv0id/TeleTweet/
cd TeleTweet
pip3 install -r requirements.txt
vim teletweet/config.py
# setup bot token, consumer key, consumer secret, app id, app secret
python3 teletweet/tweetbot.py
```

If you want the bot to be only available to you, please setup `ALLOW_USER` with your own Telegram User ID.
Use `,` to separate.

Send `/sign_in` to bot,paste your auth code, and you're good to go!

# Docker

You can run/develop using docker. You can refer to `docker-compose.yml`

```shell
echo "{}"> env/auth.json
vim env/teletweet.env
# set these config
TOKEN=123
APP_ID=123
APP_HASH=123
CONSUMER_KEY=123123
CONSUMER_SECRET=123123
ALLOW_USER=123,1234,123123
CALLBACK_URL=http://YOUR_IP:8888/callback #your ip

docker-compose up -d

```

# Plans

- [x] support multi-user, based on oauth
- [x] help
- [x] about
- [x] start
- [x] multi photo

# Credits

* [twauth-web](https://github.com/Jv0id/twauth-web)

# License

GPL 2.0__
