import telebot
from telebot import apihelper
from schedule_database import get_schedule, get_schedule_images
import users
import time
from datetime import date
import schedule_pretify
import strings


apihelper.proxy = {'https': '<proxy>', 'https': '<proxy>'}
access_token = '<access_token>'
bot = telebot.TeleBot(access_token)


def is_user(telegram_id):
    if users.get_telegram_user(telegram_id) is not None:
        return True
    else:
        return False

def user_adder(message) -> None:
    telegram_id = message.from_user.id   
    user = users.User(telegram_id=telegram_id,
                      group='?',
                      notify=False, 
                      friendly=False, 
                      last_active=time.time())
    users.add_user(user)

def is_set(user):
    if user.group != '?':
        return True
    return False

def user_from_message(message, close_threading=True):
    telegram_id = message.from_user.id
    user = users.get_telegram_user(telegram_id, close_threading)
    return user

def set_activity(user):
    user.last_active=time.time()


def check_user(message):
    """ Checks if user is in database. If it is not - adds him
        Returns True if user is set. Else: False """
    telegram_id = message.from_user.id
    if not is_user(telegram_id):
        user_adder(message)
    user = user_from_message(message)
    set_activity(user)
    if not is_set(user):
        return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    check_user(message)
    bot.send_message(message.chat.id, strings.start_hello)
    bot.send_message(message.chat.id, strings.start_info)

@bot.message_handler(commands=['help'])
def bot_help(message):
    if check_user(message):
        bot.send_message(message.chat.id, strings.command_help)
    else:
        bot.send_message(message.chat.id, strings.need_register)
        bot.send_message(message.chat.id, strings.howto_register)   

@bot.message_handler(commands=['setgroup'])
def setgroup(message):
    check_user(message)
    if len(message.text.split()) == 2:
        user = user_from_message(message, False)
        print(user)
        _, group = message.text.split()
        group = group.upper()
        users.update_user(user, group=group)

        response = strings.set_group_ok.format(group)
        bot.send_message(message.chat.id, response)
        bot.send_message(message.chat.id, strings.start_info)
    else:
        bot.send_message(message.chat.id, strings.wrong_command_usage)

@bot.message_handler(commands=['schedule'])
def send_schedule(message):
    if not check_user(message):
        bot.send_message(message.chat.id, strings.need_register)
        bot.send_message(message.chat.id, strings.howto_register)
    else:
        user = user_from_message(message)
        schedule = get_schedule(user.group)
        if schedule is None:
            bot.send_message(message.chat.id, strings.group_incorrect)
            bot.send_message(message.chat.id, strings.howto_register)
        else:
            bot.send_message(message.chat.id, strings.function_not_made)

@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    if not check_user(message):
        bot.send_message(message.chat.id, strings.need_register)
        bot.send_message(message.chat.id, strings.howto_register)
    else:
        today = date.today().weekday()
        user = user_from_message(message)
        schedule = get_schedule(user.group)
        if schedule is None:
            bot.send_message(message.chat.id, strings.group_incorrect)
            bot.send_message(message.chat.id, strings.howto_register)
        else:
            response = schedule_pretify.daily_schedule_to_text(schedule[(today+2)%6])
            bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['scedimage'])
def schedule_image(message):
    if check_user(message):
        user = user_from_message(message)
        images = get_schedule_images(user.group)

        if images is not None:
            bot.send_photo(message.chat.id, images[0])
            bot.send_photo(message.chat.id, images[1])
        else:
            bot.send_message(message.chat.id, strings.group_incorrect)
            bot.send_message(message.chat.id, strings.howto_register)
    else:
        bot.send_message(message.chat.id, strings.need_register)
        bot.send_message(message.chat.id, strings.howto_register)

@bot.message_handler(content_types=['text'])
def wrong_command(message):
    bot.send_message(message.chat.id, strings.wrong_command)


bot.polling(none_stop=True)
