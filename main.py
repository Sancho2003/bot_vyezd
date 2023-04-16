import telebot
from settings import TG_TOKEN
import buttons
import bd
import schedule
from time import sleep
from threading import Thread

bot = telebot.TeleBot(TG_TOKEN)

message_text = "Hello"
message_id = 0
button_status = ""


@bot.message_handler(commands=["start"])
def registration(message):
    user_id = message.chat.id
    if bd.user_checking(user_id):
        buttons.main_menu(message)
    else:
        bot.send_message(message.from_user.id, "Введи номер ИСУ:")
        bot.register_next_step_handler(message, get_isu_number, user_id)


@bot.message_handler(commands=["support"])
def support_info(message):
    bot.send_message(message.from_user.id,
                     "По всем техническим вопросам обращайтесь к [Саше](tg://user?id=842833101)",
                     parse_mode='Markdown')


def get_isu_number(message, user_id):
    isu_number_str = message.text
    if not isu_number_str.isnumeric() or len(isu_number_str) != 6:
        bot.send_message(message.chat.id, "Это должно быть число из 6 цифр")
        bot.register_next_step_handler(message, get_isu_number,
                                       user_id)
    else:
        isu_number = int(isu_number_str)
        if bd.isu_checking(isu_number):
            bd.add_user_id(user_id)
            bot.send_message(message.chat.id, "Здравствуй, счастливчик, здесь ты можешь узнать свой домик, команду и расписание!")
            buttons.main_menu(message)
        else:
            bot.send_message(message.chat.id, "Упс, похоже тебя нет в списках на выезд \U0001F63F")


def show_main_menu(message):
    buttons.main_menu(message)


@bot.message_handler(content_types=["text"])
def get_words(message):
    global message_text, message_id
    message_text = message.text
    message_id = int(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == buttons.timetable)
def timetable_function(call):
    bot.send_photo(call.from_user.id, open("Расписание.jpg", "rb"))
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.settlement)
def settlement_function(call):
    bot.send_photo(call.from_user.id, open("Расселение.jpg", "rb"))
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.teams)
def teams_function(call):
    bot.send_photo(call.from_user.id, open("Команды.jpg", "rb"))
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.exit_button)
def back_to_menu_function(call):
    bot.send_message(call.from_user.id, text="Меню")
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    show_main_menu(call)


def send_vyezd():
    users = bd.get_user_id()
    reminding = "Добро пожаловать в Atomic Berry. Надеемся, что за время вашего пребывания в городе вас посетят только позитивные эмоции \U0001F64B\U0001F3FB\u200D\u2642\uFE0F"
    for user in users:
        bot.send_message(user, reminding)


def send_obed():
    users = bd.get_user_id()
    reminding = "Товарищи, в Atomic Berry объявляется обед. Просим пройти в столовую \U0001F37D"
    for user in users:
        bot.send_message(user, reminding)


def send_uzhin():
    users = bd.get_user_id()
    reminding = "Уважаемые гости, просим пройти вас в столовую на ужин \U0001F958"
    for user in users:
        bot.send_message(user, reminding)


def send_zavtrak():
    users = bd.get_user_id()
    reminding = "Доброе утро, товарищи, напоминаем вам, что вы уже можете пройти в столовую на завтрак или \U0001F95E"
    for user in users:
        bot.send_message(user, reminding)


def send_uezd():
    users = bd.get_user_id()
    reminding = "Atomic Berry не прощается с вами, а говорит лишь до свидания \U0001F44B"
    for user in users:
        bot.send_message(user, reminding)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


schedule.every().saturday.at("19:15").do(send_uzhin)
schedule.every().sunday.at("09:30").do(send_zavtrak)
schedule.every().sunday.at("12:20").do(send_uezd)
Thread(target=schedule_checker).start()
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        sleep(3)
        print(e)


#"Добро пожаловать в Atomic Berry. Надеемся, что за время вашего пребывания в городе вас посетят только позитивные эмоции \U0001F64B\U0001F3FB\u200D\u2642\uFE0F"
#"Atomic Berry не прощается с вами, а говорит лишь до свидания \U0001F44B"
#"Товарищи, в Atomic Berry объявляется обед. Просим пройти в столовую \U0001F37D"
#"Уважаемые гости, просим пройти вас в столовую на ужин \U0001F958"
#"Доброе утро, товарищи, напоминаем вам, что вы уже можете пройти в столовую на завтрак или \U0001F95E"