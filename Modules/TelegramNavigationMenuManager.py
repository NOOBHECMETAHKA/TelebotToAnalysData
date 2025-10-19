from telebot import types, TeleBot
from Modules.TimeWorkDayManager import TimeWorkDayManager

class TGNavigationMenuManager():
    def __init__(self):
        self.navIndex = 0
        self.main_menu_content = {
            0: {
                "flew_row": 2,
                "menu": [
                    "Доброе утро (Поставить счётчик времени)", #
                    "Доброго вечера (Закончить рабочий день)", #
                    # "Попросить график работника", #
                    # "Загрузить данные для анализа", #
                    # "Удалить все данные", #
                ]
            },
        }
    
    def set_default(self):
        self.navIndex = 0

    def navigation(self, message, telebot: TeleBot):
        match message.text:
            case "Доброе утро (Поставить счётчик времени)":
                telebot.send_message(message.chat.id, TimeWorkDayManager().get_message_good_morning())
                self.set_default()
            
            case "Доброго вечера (Закончить рабочий день)":
                telebot.send_message(message.chat.id, TimeWorkDayManager().get_message_good_evening())
                telebot.send_message(message.chat.id, TimeWorkDayManager().get_statistic_of_day())
                self.set_default()


    #Создаёт меню исходя из указателя
    def chatMenuCreator(self) -> types.ReplyKeyboardMarkup:
        '''
        Получается индекс и исходя из него получает необходимое меню
        '''
        keyboard = types.ReplyKeyboardMarkup(row_width=self.main_menu_content[self.navIndex]["flew_row"])
        for btn in self.main_menu_content[self.navIndex]["menu"]:
            keyboard.add(types.KeyboardButton(btn))
        return keyboard
    
    def chatMenuCreatorByIndex(self, index: int) -> types.ReplyKeyboardMarkup:
        '''
        Получается индекс и исходя из него получает необходимое меню
        '''
        keyboard = types.ReplyKeyboardMarkup(row_width=self.main_menu_content[index]["flew_row"])
        for btn in self.main_menu_content[self.navIndex]["menu"]:
            keyboard.add(types.KeyboardButton(btn))
        return keyboard

