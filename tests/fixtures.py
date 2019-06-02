from pytest import fixture

from storages.mongo import CardManager


@fixture
def card_manager():
    return CardManager()
