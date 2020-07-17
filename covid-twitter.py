import json
import tweepy
import requests
from time import sleep
from datetime import datetime, timedelta

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
twitter = tweepy.API(auth)

contents = ['confirmed', 'cases', 'recovered', 'deaths']
last_values = []


def get_api():
    return eval(requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil/').text)


def make_local_time(data):
    t = datetime.strptime(data['data']['updated_at'], '%Y-%m-%dT%H:%M:%S.000Z') - timedelta(hours=3)
    t = t.strftime('%d-%m-%Y %H:%M:%S')
    return t


def formata_valor(content):
    content = str("{:,}".format(int(api['data'][content]))).replace(',', '.')
    return content


def formata_tweet(atualizado, lista):
    mensagem = f'''Casos de coronavírus no Brasil 🇧🇷

✅ {lista[0]} Confirmados
🚨 {lista[1]} Ativos
♻ {lista[2]} Recuperados
💀 {lista[3]} Mortes

🕐 Atualizado: {atualizado}
📊 Fonte: WHO, CDC, ECDC, NHC e DXY'''
    tags = '\n#Python #RaspberryPi #covid19 #coronavirus #Recife'
    return mensagem + tags


while True:
    api = get_api()
    values = [formata_valor(i) for i in contents]
    if values != last_values:
        twitter.update_status(formata_tweet(make_local_time(api), values))
        last_values = values

    sleep(300)
