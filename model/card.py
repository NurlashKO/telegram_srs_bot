from datetime import datetime, timedelta

level_deadlines = [
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
]


class Card:
    def __init__(self, user_id: int, question: str, answer: str):
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.level = 0
        self.deadline = datetime.now()

    def update_level(self, value):
        self.level = max(0, min(self.level + value, len(level_deadlines) - 1))
        self.deadline = datetime.now() + level_deadlines[self.level]

