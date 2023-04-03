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
        bd.add_user_id(user_id)
        bot.send_message(message.from_user.id, "Введи имя:")
        bot.register_next_step_handler(message, get_name, user_id)


@bot.message_handler(commands=["support"])
def support_info(message):
    bot.send_message(message.from_user.id, "По всем техническим вопросам обращайтесь к [Саше](tg://user?id=842833101)",
                     parse_mode='Markdown')


def get_name(message, user_id):
    name = message.text
    bot.send_message(message.from_user.id, "Введи фамилию:")
    bot.register_next_step_handler(message, get_surname, name, user_id)


def get_surname(message, name, user_id):
    surname = message.text
    bot.send_message(message.from_user.id, "Введи номер ИСУ:")
    bot.register_next_step_handler(message, get_isu_number, name, surname,
                                   user_id)


def get_isu_number(message, name, surname, user_id):
    isu_number_str = message.text
    if not isu_number_str.isnumeric() or len(isu_number_str) != 6:
        bot.send_message(message.chat.id, "Это должно быть число из 6 цифр")
        bot.register_next_step_handler(message, get_isu_number, name, surname,
                                       user_id)
    else:
        isu_number = int(isu_number_str)
        bd.add_info(user_id, name, surname, isu_number)
        bot.send_message(message.from_user.id, "Регистрация прошла успешно!")
        buttons.main_menu(message)


def show_main_menu(message):
    buttons.main_menu(message)


@bot.message_handler(content_types='text')
def get_words(message):
    global message_text, message_id
    message_text = message.text
    message_id = int(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == buttons.timetable)
def timetable_function(call):
    # a = bd.get_timetable()
    # bot.send_message(call.from_user.id, "Сейчас " + a[0] + ", локация: " + a[1])
    bot.send_message(call.from_user.id, "Скоро здесь будет расписание!")
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.settlement)
def settlement_function(call):
    bot.send_message(call.from_user.id, "Скоро здесь будет список расселения!")
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


def send_reminding():
    users = bd.get_user_id()
    reminding = "НапоминалОчка"
    for user in users:
        bot.send_message(user, reminding)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


schedule.every().day.at("14:38").do(send_reminding)
Thread(target=schedule_checker).start()
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        sleep(3)
        print(e)
