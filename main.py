import telebot
from settings import TG_TOKEN
import buttons
import bd


bot = telebot.TeleBot(TG_TOKEN)

message_text = "Hello"
message_id = 0
button_status = ""


@bot.message_handler(commands=["start"])
def show_main_menu(message):
    buttons.main_menu(message)


@bot.message_handler(content_types='text')
def get_words(message):
    global message_text, message_id, button_status
    message_text = message.text
    message_id = int(message.from_user.id)
    if button_status == 'add':
        buttons.Buttons(message).creating_keyboard(message)


@bot.callback_query_handler(func=lambda call: call.data == buttons.timetable)
def timetable_function(call):
    a = bd.get_timetable()
    bot.send_message(call.from_user.id, "Сейчас " + a[0] + ", локация: " + a[1])
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.settlement)
def settlement_function(call):
    bot.send_message(call.from_user.id, text="Пока ничего нет")
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.exit_button)
def back_to_menu_function(call):
    bot.send_message(call.from_user.id, text="Меню")
    show_main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.add)
def approve_button_func(call):
    global button_status
    if button_status == "add":
        bd.add_to_db(message_text, message_id)
        bot.send_message(call.from_user.id, "Готово")


bot.polling(none_stop=True, interval=0)
