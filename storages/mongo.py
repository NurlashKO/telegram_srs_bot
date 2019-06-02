from datetime import timedelta, datetime
from os import getenv
from typing import Dict

from pymongo import MongoClient
from telebot.types import Message

LEVEL_DEADLINES = (
    timedelta(seconds=0),
    timedelta(hours=1),
    timedelta(hours=3),
    timedelta(hours=8),
    timedelta(days=1),
    timedelta(days=3),
    timedelta(weeks=1),
    timedelta(weeks=2),
    timedelta(days=30),
    timedelta(days=60),
    timedelta(days=120),
    timedelta(days=240),
    timedelta(days=480),
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CardManager(metaclass=Singleton):
    def __init__(self):
        username = getenv('MONGO_USERNAME')
        password = getenv('MONGO_PASSWORD')
        self.cards = MongoClient(f'mongodb://{username}:{password}@mongo:27017/').db.cards

    def add(self, chat_id: int, question, answer) -> None:
        card = {
            'chat_id': chat_id,
            'question': {'from_chat_id': question['chat']['id'], 'message_id': question['message_id']},
            'answer': {'from_chat_id': answer['chat']['id'], 'message_id': answer['message_id']},
            'level': 0,
            'deadline': datetime.now().timestamp()
        }
        self.cards.insert_one(card)

    def count(self):
        return self.cards.count_documents({})

    def update_level(self, card, value):
        card['level'] = max(0, min(card['level'] + value, len(LEVEL_DEADLINES) - 1))
        card['deadline'] = (datetime.now() + LEVEL_DEADLINES[card['level']]).timestamp()
        self.cards.update_one({'_id': card['_id']}, {'$set': card}, upsert=False)

    def current_top_for(self, chat_id: int) -> Dict:
        return self.cards.find(
            {'chat_id': chat_id}
        ).sort(key_or_list='deadline', direction=1)[0]


class UserManager(metaclass=Singleton):
    LEARNING_STATE = 'learning'
    ADD_CARD_QUESTION = 'add_card_question'
    ADD_CARD_ANSWER = 'add_card_answer'

    def __init__(self):
        self.users = MongoClient('mongodb://user:pass@mongo:27017/').db.users

    def create(self, chat_id: int, user_id: int) -> None:
        user = {'chat_id': chat_id, 'user_id': user_id, 'state': self.LEARNING_STATE, 'tmp_message': {}}
        self.users.insert_one(user)

    def getUser(self, chat_id: int, user_id: int):
        return self.users.find({'chat_id': chat_id, 'user_id': user_id})[0]

    def setUserState(self, chat_id: int, user_id: int, state):
        self.users.update_one({'chat_id': chat_id, 'user_id': user_id}, {'$set': {'state': state}}, upsert=False)

    def saveQuestion(self, message: Message):
        self.users.update_one({'chat_id': message.chat.id, 'user_id': message.from_user.id},
                              {'$set': {
                                  'tmp_message': {'chat': {'id': message.chat.id}, 'message_id': message.message_id}}},
                              upsert=False)

    def getSavedQuestion(self, message: Message):
        return self.users.find({'chat_id': message.chat.id, 'user_id': message.from_user.id})[0]['tmp_message']
