from Modules.DatabaseManager import DataBaseManager
from datetime import datetime
from enum import Enum
import json


class TimesOfDay(Enum):
    morning = 0
    evening = 1

class TimeWorkDayManager:
    def __init__(self, user_link):
        self.user_link = user_link
        self.buffer_link = "buffer.json"
        self.local_data_work_time = {
            "current_time": "",
            "current_date": "",
            "start_day_date": "",
            "start_day_time": "",
            "end_day_date": "",
            "end_day_time": "",
        }
        self.period_of_time = ""

    def write_to_buffer(self, data, link):
        with open(link, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def read_from_buffer(self, link):
        data = {}
        with open(link, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data

    
    def get_message_good_morning(self) -> str:
        self.set_current_period_of_time(TimesOfDay.morning)
        return f"({self.period_of_time.strftime("%H:%M:%S")}) | Доброе утро! Начала рабочего дня установлено)"
    
    def get_message_good_evening(self) -> str:
        is_data_corrected = self.set_current_period_of_time(TimesOfDay.evening)
        if is_data_corrected:
            return f"({self.period_of_time.strftime("%H:%M:%S")}) | Приятного вечера! Конец рабочего дня)"
        else:
            return "Начала рабочего дня не было установлено"
    

    def get_hour_minut_defferent_from_datetime(self, started_date: str, started_time: str, ended_date: str, ended_time: str) -> tuple:
        datetime_start = datetime.strptime(started_date + " " + started_time, "%d/%m/%Y %H:%M:%S")
        datetime_end = datetime.strptime(ended_date + " " + ended_time, "%d/%m/%Y %H:%M:%S")

        total_seconds = datetime_end - datetime_start
        hours = total_seconds.seconds // 3600
        minutes = (total_seconds.seconds % 3600 // 60)
        #f"Длительность времени: часы: {hours}; минут: {minutes}"
        return { "hours": hours, "minutes": minutes }

    
    def get_statistic_of_day(self) -> str:
        # Чтение данныех из локального буфера
        self.local_data_work_time = self.read_from_buffer(self.buffer_link)
        # Объявление начального сообщения
        message = ""

        # Проверяет есть ли в локальном буфере текущий пользователь
        if(self.user_link not in self.local_data_work_time):
            message = "Сегодня время работы не устанавливалось текущим пользователем"
        elif "start_day_time" not in self.local_data_work_time[self.user_link] or "start_day_date" not in self.local_data_work_time[self.user_link]:
            message = "Сегодня время работы не устанавливалось текущим пользователем"
        else:
            # Получение буфера текущего пользователя
            self.local_data_work_time = self.local_data_work_time[self.user_link]
            # Установка перенных для записи
            started_formated_time = self.local_data_work_time["start_day_time"]
            ended_formated_time = self.local_data_work_time["end_day_time"]

            message = f"Результаты работы дня:\nНачало работы: {started_formated_time}\nКонец работы: {ended_formated_time}\n"
            date_diff = self.get_hour_minut_defferent_from_datetime(
                self.local_data_work_time["start_day_date"],
                self.local_data_work_time["start_day_time"],
                self.local_data_work_time["end_day_date"],
                self.local_data_work_time["end_day_time"]
            ) 
            message += f"Длительность рабочего дня: {date_diff["hours"]} (час.), {date_diff["minutes"]} (минут.)"
        return message
    
    # Установка времени в локальное хранилище в зависимости от диапозона времени
    def set_current_period_of_time(self, time_of_day: TimesOfDay) -> bool:
        is_data_corrected = True
        # Получение текущего времени из буфера
        self.local_data_work_time = self.read_from_buffer(self.buffer_link)

        # Если полученные данные из буфера по корретному пользователю не существуют устанавливаем текущий массив
        if self.user_link not in self.local_data_work_time:
            self.local_data_work_time[self.user_link] = {}

        # Установка текущего времени в буфер
        self.local_data_work_time[self.user_link]["current_time"] = datetime.now().strftime("%d/%m/%Y")
        self.local_data_work_time[self.user_link]["current_date"] = datetime.now().strftime("%H:%M:%S")
        
        # Установка текущего времени в оперативную памятья для дальнейшего вывода
        self.period_of_time = datetime.now()

        # В зависимости от текущего положения времени
        match(time_of_day):
            case TimesOfDay.morning:
                # Запись утренного времени и удалиние старых позиций
                self.local_data_work_time[self.user_link]["start_day_date"] = datetime.now().strftime("%d/%m/%Y")
                self.local_data_work_time[self.user_link]["start_day_time"] = datetime.now().strftime("%H:%M:%S")
                self.local_data_work_time[self.user_link]["end_day_date"] = ""
                self.local_data_work_time[self.user_link]["end_day_time"] = ""

            case TimesOfDay.evening:                
                self.local_data_work_time[self.user_link]["end_day_date"] = datetime.now().strftime("%d/%m/%Y")
                self.local_data_work_time[self.user_link]["end_day_time"] = datetime.now().strftime("%H:%M:%S")

                if "start_day_date" not in self.local_data_work_time[self.user_link]:
                    is_data_corrected = False
                if "start_day_time" not in self.local_data_work_time[self.user_link]:
                    is_data_corrected = False
        
        self.write_to_buffer(self.local_data_work_time, self.buffer_link)
        return is_data_corrected

        
    
