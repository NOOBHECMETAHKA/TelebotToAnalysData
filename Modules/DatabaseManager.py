from peewee import *
from datetime import date, time, datetime


db = SqliteDatabase('db.db')

class Person(Model):
    time_of_started = TimeField()
    time_of_end = TimeField()
    date_of_work = DateField()
    user_link = CharField()

    class Meta:
        database = db 

class DataBaseManager:    
    def __init__(self, user_link):
        self.user_link = user_link

    def create_person(self, datetime_started: datetime, datetime_ended: datetime):
        db.connect([Person])
        Person.create_table()
        new_person = Person(
            time_of_started = datetime_started.time(),
            time_of_end = datetime_ended.time(),
            date_of_work = datetime_ended.date(),
            user_link = self.user_link
        )
        new_person.save()
        db.close()


        
    

    
    


   
    
        