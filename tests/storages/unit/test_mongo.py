def test_add_card(mongodb, card_manager):
    card_manager.add(user_id=1, question='2+2?', answer='4')
    assert card_manager.count() == 1
