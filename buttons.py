import telebot
from settings import TG_TOKEN


bot = telebot.TeleBot(TG_TOKEN)


class Buttons:
    def __init__(self, call):
        self.exit_b = telebot.types.InlineKeyboardButton(
            text=exit_button,
            callback_data=exit_button)
        self.bot = telebot.TeleBot(TG_TOKEN)
        self.new_keyboard = telebot.types.InlineKeyboardMarkup()
        self.new_keyboard.add(self.exit_b)

    def creating_keyboard(self, call):
        self.bot.send_message(call.from_user.id, text="Выберите:",
                              reply_markup=self.new_keyboard)


exit_button = "В меню"
timetable = "Расписание"
settlement = "Расселение"
reminding = "Напоминание"


@bot.message_handler(content_types="text")
def main_menu(message):
    user_markup = telebot.types.InlineKeyboardMarkup()
    timetable_b = telebot.types.InlineKeyboardButton(
            text=timetable,
            callback_data=timetable)
    settlement_b = telebot.types.InlineKeyboardButton(
            text=settlement,
            callback_data=settlement)
    user_markup.add(timetable_b)
    user_markup.add(settlement_b)
    bot.send_message(message.from_user.id, text="Выберите:",
                     reply_markup=user_markup)
