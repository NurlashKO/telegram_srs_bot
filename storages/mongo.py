from pymongo import MongoClient


class CardManager:
    def __init__(self):
        self.cards = MongoClient('mongodb://user:pass@mongo:27017/').db.cards

    def add(self, user_id: int, question: str, answer: str) -> None:
        card = {'user_id': user_id, 'question': question, 'answer': answer}
        self.cards.insert_one(card)

    def count(self):
        return self.cards.count_documents({})
