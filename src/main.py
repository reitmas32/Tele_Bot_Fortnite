from asyncio import sleep
import telebot
import config
import requests
import json

from PIL import Image
from io import BytesIO

class Items_Fortnite:
    section_name = ''
    data = {}

    def __init__(self, section_name, data):
        self.section_name = section_name
        self.data = data

# Collections
outfits = []
backpacks = []
emotes = []
pickaxes = []

# Data in JSON format
json_object = {}

#Telegram Bot
bot = telebot.TeleBot(config.TELEBOT_KEY)

# Load items of sections
def middelware_shop(section: str, type_item: str) -> dict:
    data = {}

    if json_object['status'] == 200:
        print('Tienda encontrada: ' + json_object['data']['date'])

        if json_object['data'][section]:
            featured = json_object['data'][section]['entries']

            for f in featured:
                if f['items']:

                    for item in f['items']:
                        if item['type']['value'] == type_item:
                            msg = 'Item: ' + item['name'] + '\n'

                            if type_item == 'emote':
                                response = requests.get(item['images']['icon'])
                            else:
                                response = requests.get(item['images']['smallIcon'])
                            img = Image.open(BytesIO(response.content))
                            data[msg] = img
    return data

def load_outfits(type_item: str):

    collection = []

    shop_featured = Items_Fortnite('featured', middelware_shop('featured', type_item))
    collection.append(shop_featured)

    shop_daily = Items_Fortnite('daily', middelware_shop('daily', type_item))
    collection.append(shop_daily)

    shop_specialFeatured = Items_Fortnite('specialFeatured', middelware_shop('specialFeatured', type_item))
    collection.append(shop_specialFeatured)

    shop_specialDaily = Items_Fortnite('specialDaily', middelware_shop('specialDaily', type_item))
    collection.append(shop_specialDaily)

    return collection

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello Im the Bot to see Shop of Fortnite \n My commands: \n /outfits, /pickaxes /backpacks /emotes and the parameter section=[daily, featured, specialFeatured, specialDaily]')
    bot.send_message(message.chat.id, "Example: /outfits daily")


@bot.message_handler(commands=['outfits'])
def send_outfits(message):

    for items in outfits:
        if message.text == '/outfits ' + items.section_name:
            print('Send Outfits Section: ' + items.section_name)
            bot.send_message(message.chat.id, 'Send Outfits Section: ' + items.section_name)
            for k in items.data:
                bot.send_message(message.chat.id, k)
                bot.send_photo(message.chat.id, items.data[k])

@bot.message_handler(commands=['backpacks'])
def send_backpacks(message):

    for items in backpacks:
        if message.text == '/backpacks ' + items.section_name:
            print('Send Backpacks Section: ' + items.section_name)
            bot.send_message(message.chat.id, 'Send Backpacks Section: ' + items.section_name)
            for k in items.data:
                bot.send_message(message.chat.id, k)
                bot.send_photo(message.chat.id, items.data[k])

@bot.message_handler(commands=['emotes'])
def send_emotes(message):

    for items in emotes:
        if message.text == '/emotes ' + items.section_name:
            print('Send Emotes Section: ' + items.section_name)
            bot.send_message(message.chat.id, 'Send Emotes Section: ' + items.section_name)
            for k in items.data:
                bot.send_message(message.chat.id, k)
                bot.send_photo(message.chat.id, items.data[k])

@bot.message_handler(commands=['pickaxes'])
def send_pickaxes(message):

    for items in pickaxes:
        if message.text == '/pickaxes ' + items.section_name:
            print('Send pickaxes Section: ' + items.section_name)
            bot.send_message(message.chat.id, 'Send pickaxes Section: ' + items.section_name)
            for k in items.data:
                bot.send_message(message.chat.id, k)
                bot.send_photo(message.chat.id, items.data[k])
            

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

def main():
    x = requests.get('https://fortnite-api.com/v2/shop/br?language=es')
    json_object.update(json.loads(x.text))

    outfits.extend(load_outfits('outfit'))
    backpacks.extend(load_outfits('backpack'))
    emotes.extend(load_outfits('emote'))
    pickaxes.extend(load_outfits('pickaxe'))

    bot.infinity_polling()


main()