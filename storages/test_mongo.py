from mongo import CardManager


def test_add_card():
    card_manager = CardManager()
    card_manager.add(user_id=1, question='2+2?', answer='4')
    assert card_manager.count() == 1


test_add_card()
