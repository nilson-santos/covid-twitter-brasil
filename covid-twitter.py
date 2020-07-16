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

last_update = ''

while True:
    r = requests.get('https://covid19-brazil-api.now.sh/api/report/v1/brazil/')
    api = eval(r.text)

    local_time = datetime.strptime(api['data']['updated_at'], '%Y-%m-%dT%H:%M:%S.000Z') - timedelta(hours=3)
    local_time = local_time.strftime('%d/%m/%Y %H:%M:%S')
    if local_time != last_update:
        confirmed = str("{:,}".format(int(api['data']['confirmed']))).replace(',', '.')
        active = str("{:,}".format(int(api['data']['cases']))).replace(',', '.')
        recovered = str("{:,}".format(int(api['data']['recovered']))).replace(',', '.')
        deaths = str("{:,}".format(int(api['data']['deaths']))).replace(',', '.')

        msg = f'''*Casos coronavírus no Brasil 🇧🇷*
            
✅ *{confirmed}* Confirmados
🚨 *{active}* Ativos
♻ *{recovered}* Recuperados
💀 *{deaths}* Mortes
            
🕐 *Atualizado * {local_time}
📊 *Fonte: *WHO, CDC, ECDC, NHC e DXY'''

        caption = '\n#Python #RaspberryPi #covid19 #coronavirus #Recife'
        twitter.update_status(msg + caption)
        last_update = local_time

    sleep(300)
