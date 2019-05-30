from datetime import datetime


class Card(object):
    def __init__(self, user_id, top, bottom):
        self.user_id = user_id
        self.top = top
        self.bottom = bottom
        self.level = 0
        self.deadline = datetime.now()
