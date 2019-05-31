from datetime import timedelta, datetime

from pymongo import MongoClient

level_deadlines = (
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


class CardManager:
    def __init__(self):
        self.cards = MongoClient('mongodb://user:pass@mongo:27017/').db.cards

    def add(self, user_id: int, question: str, answer: str) -> None:
        card = {'user_id': user_id, 'question': question, 'answer': answer, 'level': 0,
                'deadline': datetime.now().timestamp()}
        self.cards.insert_one(card)

    def count(self):
        return self.cards.count_documents({})

    def update_level(self, card, value):
        print(card)
        card["level"] = max(0, min(card["level"] + value, len(level_deadlines) - 1))
        card["deadline"] = (datetime.now() + level_deadlines[card["level"]]).timestamp()
        self.cards.update_one({'_id': card["_id"]}, {'$set': card}, upsert=False)
