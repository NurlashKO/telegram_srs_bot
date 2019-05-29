cards = []


def add_card(message: str):
    if len(message.split('-/-')) != 2:
        raise ValueError(
            'Wrong command format.\nMessage must contain exactly one `-/-` separator and non empty text on both sides.')

    first_part, second_part = message.split('-/-')
    if not first_part:
        raise ValueError('Wrong command format.\nFirst part is empty')
    if not second_part:
        raise ValueError('Wrong command format.\nSecond part is empty')
    cards.append((first_part, second_part))
    return first_part, second_part


def next_card():
    global cards
    card = cards[-1]
    cards.pop()
    cards = [card] + cards
    return card
