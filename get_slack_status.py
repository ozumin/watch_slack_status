# coding: UTF-8
import requests
import pickle
import json
import os
import slack
from os.path import join, dirname
from dotenv import load_dotenv

# TOKEN取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN") # 環境変数の値をAPに代入
CHANNEL_ID = os.environ.get("CHANNEL_ID") # 送りたいslackのチャンネルID
client = slack.WebClient(token=TOKEN)

# 前回の結果の読み取り
if os.path.exists("statuses.pickle"):
    with open('statuses.pickle', 'rb') as f:
        last_statuses = pickle.load(f)

# slack API叩く
response = requests.get('https://slack.com/api/users.list?token=' + TOKEN)

# 必要な情報をとる
member_list = json.JSONDecoder().decode(response.text)['members']
statuses = {}
for member in member_list:
    statuses[member['name']] = member['profile']['status_text']

# 結果の保存
with open('statuses.pickle', 'wb') as f:
    pickle.dump(statuses, f)

# 前回との差分をslackに送る
if last_statuses:
    for s in statuses:
        if statuses[s] != last_statuses[s]:
            response = client.chat_postMessage(channel=CHANNEL_ID, text=s + ': ' + statuses[s])