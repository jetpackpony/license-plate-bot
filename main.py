import os
import telebot
import regex as re
import pandas as pd
import time
import datetime

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
SPREADSHEET_URL = os.environ.get("SPREADSHEET_URL")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

df = pd.read_csv(
    SPREADSHEET_URL,
    dtype={
        'Цифры госномера для быстрого поиска': 'string',
        'Дом': 'string',
        'Квартира': 'string'
    })


@bot.message_handler(commands=['help', '?'])
def main(message):
    bot.send_message(message.chat.id,
                     'Чтобы определить свой или чужой автомобиль, введите цифры его госномера, без букв')


@bot.message_handler()
def main(message):
    # Обрабатываем только те сообщения, которые целиком состоят из 3 или более цифр.
    if re.match('^[0-9]{3,}$', message.text):
        filtered_df = df.loc[df['Цифры госномера для быстрого поиска'].str.contains(message.text,
                                                                                    na=False, regex=False)]
        if filtered_df.shape[0] > 0:
            for index, row in filtered_df.iterrows():
                bot.send_message(message.chat.id,
                                 f"СВОЙ: {row['Госномер']} / {row['Марка']} / {row['Владелец']} / " +
                                 f"д.{row['Дом']} кв.{row['Квартира']} / {row['Телефон']}")
        else:
            bot.send_message(message.chat.id,
                             f"ЧУЖОЙ: Автомобиль с госномером {message.text} не найден в списке.")
    else:
        pass


while True:
    try:
        print("Polling is starting...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"{datetime.datetime.now()}: {e}")
        time.sleep(5)
