from model.card import Card

cards = [Card('1', 'q', 'a')]


def add_card(user_id: int, message: str):
    if len(message.split('-/-')) != 2:
        raise ValueError(
            'Wrong command format.\nMessage must contain exactly one `-/-` separator and non empty text on both sides.')

    first_part, second_part = message.split('-/-')
    if not first_part:
        raise ValueError('Wrong command format.\nFirst part is empty')
    if not second_part:
        raise ValueError('Wrong command format.\nSecond part is empty')
    cards.append(Card(user_id, first_part, second_part))
    return first_part, second_part


def current_top():
    return min(cards, key=lambda card: card.deadline)


def guess_wrong(card):
    cards.remove(card)
    card.update_level(-1)
    cards.append(card)


def guess_correct(card):
    cards.remove(card)
    card.update_level(1)
    cards.append(card)
