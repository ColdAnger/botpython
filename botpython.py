from re import I
import telebot
import requests
from googlesearch import search #pip instal google
from bs4 import BeautifulSoup as BS
from telebot import types

i = 0
msg_search = ""
bot = telebot.TeleBot('5534545457:AAEGLr00sJ5Ur1dqwbZN33or0vCOsdiiAlk')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Здавствуйте, <b>{message.from_user.first_name} {message.from_user.last_name}</b>. Для начала работы введите команду /help'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True, row_width= 1)
    but1 = types.KeyboardButton("Краткая текстовая справочная информация")
    but2 = types.KeyboardButton("Более подробная информация из других источников")
    but3 =  types.KeyboardButton("Поиск информационного видео")
    markup.add(but1, but2, but3)
    bot.send_message(message.chat.id, 'Выберете какую информацию вы хотите получить от бота', reply_markup= markup)

@bot.message_handler(content_types='text')
def func(message):
    if message.text == "Краткая текстовая справочная информация":
        url = 'http://www.turbopro.ru/index.php/python-kratkij-spravochnik'
        r = requests.get(url)
        soup = BS(r.text, 'html.parser')
        button_all = soup.find('div', class_='sppb-addon-content sppb-tab sppb-modern-tab sppb-tab-nav-left').find('ul', class_='sppb-nav sppb-nav-modern')
        button_list = [i.text for i in button_all]
        markup = types.InlineKeyboardMarkup()
        count = 0
        for i in button_list:
            markup.add(types.InlineKeyboardButton(i,callback_data = str(count)))
            count += 1
        bot.send_message(message.chat.id, 'Выберите, о чем вы бы хотели узнать', reply_markup=markup)
    elif message.text == "Более подробная информация из других источников":
        msg = bot.send_message(message.chat.id, text="Введите запрос на информацию") 
        bot.register_next_step_handler(msg, select_2)
    elif message.text == "Поиск информационного видео":
        msg = bot.send_message(message.chat.id, "На какую тему вы бы хотели увидеть видео?")
        bot.register_next_step_handler(msg, select_3)
    else:
        bot.send_message(message.chat.id, text="Функционал бота ограничен,введите /help и сделайте выбор")
"""        
def select_1(message = "Справочная краткая информация"):
    url = 'http://www.turbopro.ru/index.php/python-kratkij-spravochnik'
    r = requests.get(url)
    soup = BS(r.text, 'html.parser')
    button_all = soup.find('div', class_='sppb-addon-content sppb-tab sppb-modern-tab sppb-tab-nav-left').find('ul', class_='sppb-nav sppb-nav-modern')
    button_list = [i.text for i in button_all]
    markup = types.InlineKeyboardMarkup()
    count = 0
    for i in button_list:
        markup.add(types.InlineKeyboardButton(i,callback_data = str(count)))
        count += 1
    bot.send_message(message.chat.id, 'Выберите, о чем вы бы хотели узнать', reply_markup=markup)
"""    
     
def select_2(message):
    global i
    global msg_search
    if message.text == "Нет":
        bot.send_message(message.chat.id, 'Надеюсь я вам помог, если нужна еще инфомация, то введите /help и сделайте выбор')
        i = 0
        return
    x = 'Вот что было найдено по вашему запросу'
    list_link = ["в pythonworld.ru", "в pythonru.com", "в docs-python.ru", "в metanit.com python"]
    if i == 0:
        msg_search = message.text 
    elif i>0 and i<3:
        x = "Вот еще информация по вашему запросу"
    elif i==3:
        x = "Это вся информация которой я владею по этой теме"
        msg_search = ""
    b = str(list(search(msg_search + list_link[i], tld="co.in", num=10, stop=1, pause=1)))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейдите по ссылке", url = b[2:-2]))
    bot.send_message(message.chat.id, x, reply_markup= markup)
    i += 1 
    if i == 4:
        bot.send_message(message.chat.id, 'К сожалению фунционал бота ограничен, и на даный момент это вся информация,\
        которую я вам могу придоставить по вашему запросу. Введите /help и попробуйте сформулировать запрос иначе или возможно \
        вы сможете найти нужную видео информацию')
        i = 0        
    elif i<4 and i>0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True, row_width= 2)
        but1 = types.KeyboardButton("Да")
        but2 = types.KeyboardButton("Нет")
        markup.add(but1, but2)
        msg = bot.send_message(message.chat.id, 'Подыскать информацию в других источниках ', reply_markup= markup)
        bot.register_next_step_handler(msg, select_2)

def select_3(message):
    b = str(list(search(message.text + "Python в youtube.com", tld="co.in", num=10, stop=1, pause=1)))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейдите по ссылке", url = b[2:-2]))
    bot.send_message(message.chat.id, 'Вот что было найдено по вашему запросу', reply_markup= markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_function1(callback_obj):
    url = 'http://www.turbopro.ru/index.php/python-kratkij-spravochnik'
    r = requests.get(url)
    soup = BS(r.text, 'html.parser')
    content_all = soup.find('div', class_='sppb-tab-content sppb-tab-modern-content')
    content_list = [i.text for i in content_all]
    bot.send_message(callback_obj.from_user.id, content_list[int(callback_obj.data)] + "\n Для поика дополнительной информации введите /help и сделайте выбор")
    
bot.polling(non_stop=True)