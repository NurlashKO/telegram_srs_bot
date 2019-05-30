from typing import Tuple
from storages.mongo import Card


def add_card(user_id: int, message: str) -> Tuple[str, str]:
    if len(message.split('-/-')) != 2:
        raise ValueError(
            'Wrong command format.\nMessage must contain exactly one `-/-` separator and non empty text on both sides.')

    first_part, second_part = message.split('-/-')
    if not first_part:
        raise ValueError('Wrong command format.\nFirst part is empty')
    if not second_part:
        raise ValueError('Wrong command format.\nSecond part is empty')
    Card(question=first_part, answer=second_part, user=user_id).save()
    return first_part, second_part


def current_top():
    return cards[-1]


def next_card():
    global cards
    card = cards[-1]
    cards.pop()
    cards = [card] + cards
    return cards[-1]
