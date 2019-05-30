from datetime import datetime


class Card:
    def __init__(self, user_id: int, question: str, answer: str):
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.level = 0
        self.deadline = datetime.now()
