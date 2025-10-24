import telebot
from datetime import datetime
from Modules.TelegramNavigationMenuManager import TGNavigationMenuManager

bot = telebot.TeleBot("5498449179:AAFiwoLz1zwBU6aHhOI6FCWQSFK-yqvHFL0", parse_mode=None)

# Определяем список команд и их описание
commands = [
    telebot.types.BotCommand("/start", "Запустить бота"),
    telebot.types.BotCommand("/menu", "Вызвать меню"),
    telebot.types.BotCommand("/gm", "Доброе утро!"),
    telebot.types.BotCommand("/ge", "Добрый вечер!"),
]

# Устанавливаем команды
bot.set_my_commands(commands)

if __name__ == "__main__":
    menu_manager = TGNavigationMenuManager()

    @bot.message_handler(commands=['start', "menu"])
    def start_menu(message):
        print(f"Индификатор чата: {message.from_user.id}; Ссылка на пользователя: t.me/{message.from_user.username}")
        bot.reply_to(message, "Выберите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())

    @bot.message_handler(content_types="text")
    def main_function(message):
        print(f"Индификатор чата: {message.from_user.id}; Ссылка на пользователя: t.me/{message.from_user.username}")
        menu_manager.navigation(message=message, telebot=bot)
        bot.reply_to(message, "Выберите функцию на панели!", reply_markup=menu_manager.chatMenuCreator())

bot.infinity_polling()