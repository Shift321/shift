import telebot
from telebot import types
import re
from sql import cursor, conn
from constants import texts, states_telegram,medicines_message
import asyncio

bot = telebot.TeleBot('1126948014:AAGz7uad4rWOuE4wUX7LyisWCl2PdsFjzuA')

markup = types.ReplyKeyboardMarkup()
markup.row("Список","Поиск")
markup.row("Список по ав","Поиск по ав") 
markup_cancel = types.ReplyKeyboardMarkup()
markup_cancel.row("Отмена")

def handle_search_as(message):                                                                                        # функция для поиска по активному веществу
    cursor.execute(f"SELECT * FROM medicines WHERE active_substance LIKE '%{message.text}%'")
    text = cursor.fetchall()
    if message.text == '':
        bot.send_message(message.chat.id, texts["exist"],reply_markup=markup)
        return
    else:
        if text == []:                                                                       # проверка есть ли препарат с таким активным веществом в базе
            bot.send_message(message.chat.id, texts["no_medicines_with_this_av_name"],reply_markup=markup)
            states_telegram[message.from_user.id] = "search_as"
            return
        for x in range(len(list(text))):
            message_of_search_as =f"""Действущее вещество: {text[x][0]}\nНазвание препарата: {text[x][1]}\nОписание: {text[x][2]}"""
    states_telegram[message.from_user.id] = "menu"
    bot.send_message(message.chat.id, message_of_search_as,reply_markup=markup)


def handle_search(message):                                                                                           # функция для поиска по названию
    search_as_sql = f"SELECT * FROM medicines WHERE medicines_name LIKE '%{message.text}%'"
    cursor.execute(search_as_sql)
    text = cursor.fetchall()
    if message.text == '':
        bot.send_message(message.chat.id, texts["exist"],reply_markup=markup)
        return
    else:
        if text == []:
            bot.send_message(message.chat.id, texts["no_medicines_with_this_name"],reply_markup=markup)                        # проверка есть ли такой препарат в базе
            states_telegram[message.from_user.id] = "search"
            return
        for x in range(len(list(text))):
            message_of_search_as = f"""Действущее вещество: {text[x][0]}\nНазвание препарата: {text[x][1]}\nОписание: {text[x][2]}"""
    states_telegram[message.from_user.id] = "menu"
    bot.send_message(message.chat.id,message_of_search_as,reply_markup=markup)


def handle_menu(message):                                                                                     # меню
    response = message.text.lower()
    if response == "меню":
        states_telegram[message.from_user.id] = "menu"
        bot.send_message(message.chat.id, texts["text_for_users"],reply_markup=markup)
    elif response == "поиск по ав":
        states_telegram[message.from_user.id] = "search_as"
        bot.send_message(message.chat.id, "Введите название действующего вещества,которое хотите посмотреть.",reply_markup=markup_cancel)
    elif response == "поиск":
        states_telegram[message.from_user.id] = "search"
        bot.send_message(message.chat.id, "Введите название препарата ,которое хотите посмотреть.",reply_markup=markup_cancel)
    elif response == "список по ав":
        cursor.execute("SELECT active_substance FROM medicines order by active_substance ASC")
        names = cursor.fetchall()
        msg = ""
        for x in names:
            msg += ''.join(x)+"\n"
        bot.send_message(message.chat.id,msg,reply_markup=markup_cancel)
    elif response == "список":
        cursor.execute("SELECT medicines_name FROM medicines order by medicines_name ASC")
        names = cursor.fetchall()
        msg = ""
        for x in names:
            msg += ''.join(x)+"\n"
        bot.send_message(message.chat.id,msg,reply_markup=markup_cancel)    
    else:
        bot.send_message(message.chat.id,texts["exist"])
def app_telegram():
    @bot.message_handler(content_types=['text'])
    def chose_handler(message):
            response = message.text.lower()
            if message.from_user.id not in states_telegram:
                states_telegram[message.from_user.id] = "menu"
                bot.send_message(message.chat.id,texts["text_for_users"],reply_markup=markup)
            if response == "отмена":
                states_telegram[message.from_user.id] = "menu"
                bot.send_message(message.chat.id,texts["text_for_users"],reply_markup=markup)
            elif states_telegram[message.from_user.id] == "menu":
                handle_menu(message)
            elif states_telegram[message.from_user.id] == "search_as":                                              # функция для поиска по активному веществу
                handle_search_as(message)
            elif states_telegram[message.from_user.id] == "search":                                              # функция для поиска по названию препарата
                handle_search(message)

bot.polling()
