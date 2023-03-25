import telebot
from settings import TG_TOKEN
import buttons


bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=["start"])
def show_main_menu(message):
    buttons.main_menu(message)


@bot.callback_query_handler(func=lambda call: call.data == buttons.timetable)
def timetable_function(call):
    bot.send_message(call.from_user.id, text="Пока ничего нет")
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.settlement)
def settlement_function(call):
    bot.send_message(call.from_user.id, text="Пока ничего нет")
    buttons.Buttons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.exit_button)
def back_to_menu_function(call):
    bot.send_message(call.from_user.id, text="Меню")
    show_main_menu(call)


bot.polling(none_stop=True, interval=0)
