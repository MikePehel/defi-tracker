import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests
import pprint as pp
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

description = '''An example bot to showcase the discord.ext.commands extension
module.'''

coin = ''


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    send_tokens.start()


@tasks.loop(seconds=180)
async def send_tokens():
    channel = client.get_channel(840698444896272455)
    coin_list = scrapePage()
    for coin in coin_list:
        await channel.send(coin)
        time.sleep(5)
    print('/////////||||||||\\\\\\\\\\\\\\\\')


# client = commands.Bot(command_prefix='.')
# discordtoken = config('discordtoken')


# @client.event  # Posts somewhere that the bot has joined the party
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')


# @client.event  # Sends message when command is recieved
# async def on_message(message):
#     id = client.get_guild(830869440718438400)
#     if message.content.find("!price") != -1:
#         await message.channel.send("Current price is $" + update_price() + "\nCurrent market cap " + getmarketcap() + "\nTotal coins burnt " + getburn())
#     elif message.content.find("!marketcap") != -1:
#         await message.channel.send(getmarketcap())
#     elif message.content.find("!burn") != -1:
#         await message.channel.send(getburn())

df = pd.read_csv('tokens.csv')


bsc_urls = ['https://bscscan.com/tokens?ps=100',
            'https://bscscan.com/tokens?ps=100&p=2']

params = {}
headers = {}


def scrapePage():
    coin = ''
    coin_list = []
    i = 0
    with open('tokens.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['Token']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        new_tokens = []
        listings = []
        while i < 2:
            response = requests.get(
                bsc_urls[i], params=params, headers=headers)

            html = response.content.decode(response.encoding)

            soup = BeautifulSoup(html, 'html.parser')

            tickers = soup.find_all('h3', attrs={'class': 'h6 mb-0'})
            rows = soup.find_all('tr')

            ticker_dict = {}
            for row in rows:
                fields = row.find_all('td')
                price = row.select('td:nth-of-type(3)')
                for td in fields:
                    if td.h3 is not None:
                        ticker_dict['Token'] = td.h3.a.string
                    if td.a is not None:
                        ticker_dict['Link'] = "https://bscscan.com/" + \
                            td.a['href']
                volume = row.select('td:nth-of-type(5)')
                for el in volume:
                    ticker_dict['Volume'] = el.text
                market_cap = row.select('td:nth-of-type(6)')
                for el in market_cap:
                    ticker_dict['Market Cap'] = el.text
                for el in price:
                    ticker_dict['Price'] = el.text
                ticker_dict = ticker_dict.copy()
                listings.append(ticker_dict)
            token_list = []
            for token in df['Token']:
                token_list.append(token)
            for listing in listings:
                if listing['Token'] in token_list:
                    writer.writerow({'Token': listing['Token']})
                elif listing['Token'] not in token_list:
                    coin = listing['Token'] + ' | Price: ' + listing['Price'] + \
                        '\n Link: ' + listing['Link'] + \
                        '\n 24h Volume: ' + listing['Volume'] +  \
                        '\n Market Cap: ' + listing['Market Cap']
                    coin_list.append(coin)
                    writer.writerow({'Token': listing['Token']})
            i += 1
            time.sleep(5)
        pp.pprint(coin_list)
    return coin_list
    coin_list = []
    coin = ''


client.run(TOKEN)

# client.on('ready', client= > {
#     client.channels.get('840698444896272455').send('Hello here!')
# })


# @client.event
# async def send_message():
