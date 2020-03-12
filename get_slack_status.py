# coding: UTF-8
import requests
import pickle
import json
import os
import slack
from os.path import join, dirname
from dotenv import load_dotenv

# TOKEN取得
dotenv_path = join(dirname(__file__), '/home/lab/mizuo/watch_slack_status/.env')
load_dotenv(dotenv_path)
DIRPATH = os.environ.get("DIRPATH") # cron用に絶対パスにするため、リポジトリのパスを読み込む
TOKEN = os.environ.get("TOKEN") # 環境変数の値をAPに代入
CHANNEL_ID = os.environ.get("CHANNEL_ID") # 送りたいslackのチャンネルID
MY_NAME = os.environ.get("MY_NAME") # 自分のステータスは通知しない
client = slack.WebClient(token=TOKEN)

# 前回の結果の読み取り
last_statuses = ''
if os.path.exists(DIRPATH + "statuses.pickle"):
    with open(DIRPATH + 'statuses.pickle', 'rb') as f:
        last_statuses = pickle.load(f)

# slack API叩く
response = requests.get('https://slack.com/api/users.list?token=' + TOKEN)

# 必要な情報をとる
member_list = json.JSONDecoder().decode(response.text)['members']
statuses = {}
for member in member_list:
    statuses[member['name']] = member['profile']['status_emoji'] + member['profile']['status_text']

# 結果の保存
with open(DIRPATH + 'statuses.pickle', 'wb') as f:
    pickle.dump(statuses, f)

# 前回との差分をslackに送る
if last_statuses:
    for k in statuses.keys():
        if k == MY_NAME:
            pass
        else:
            if last_statuses[k] and statuses[k] != last_statuses[k]:
                response = client.chat_postMessage(channel=CHANNEL_ID, text=k + ': ' + statuses[k])
