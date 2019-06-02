from datetime import timedelta, datetime
from typing import Dict

from pymongo import MongoClient

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
        self.cards = MongoClient('mongodb://user:pass@mongo:27017/').db.cards

    def add(self, chat_id: int, question: str, answer: str) -> None:
        card = {
            'chat_id': chat_id, 'question': question, 'answer': answer, 'level': 0,
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
