from typing import Tuple

from storages.mongo import CardManager


def add_card(user_id: int, message: str) -> Tuple[str, str]:
    if len(message.split('-/-')) != 2:
        raise ValueError(
            'Wrong command format.\nMessage must contain exactly one `-/-` separator and non empty text on both sides.')

    first_part, second_part = message.split('-/-')
    if not first_part:
        raise ValueError('Wrong command format.\nFirst part is empty')
    if not second_part:
        raise ValueError('Wrong command format.\nSecond part is empty')
    CardManager().add(question=first_part, answer=second_part, user_id=user_id)
    return first_part, second_part


def current_top():
    return CardManager().cards.find().sort('deadline', 1)[0]


def guess_wrong(card):
    CardManager().update_level(card, -1)


def guess_correct(card):
    CardManager().update_level(card, 1)
