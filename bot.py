from typing import Tuple

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message

from storages.mongo import CardManager, UserManager


def set_up_bot() -> TeleBot:
    return TeleBot('849639836:AAETYUnkEBESn6EfQcxjgcC_l4c_kBDFcMY')


def set_up_markup() -> Tuple[ReplyKeyboardMarkup, ReplyKeyboardMarkup]:
    markup_question = ReplyKeyboardMarkup(row_width=1)
    markup_question.add(KeyboardButton('/show'))

    markup_pull = ReplyKeyboardMarkup(row_width=2)
    forgot_response = KeyboardButton('/hard')
    remember_response = KeyboardButton('/good')
    markup_pull.add(forgot_response, remember_response)
    return (markup_question, markup_pull,)


bot = set_up_bot()
markup_question, markup_pull = set_up_markup()
card_manager = CardManager()
user_manager = UserManager()


@bot.message_handler(commands=('start',))
def send_welcome(message: Message):
    bot.send_message(chat_id=message.chat.id, text="""Hey, I am here to help you with memorizing stuff.
User following commands to interact with me:
    /add - create new card
    /learn - get back to reviews
    /help - ...
HF ;)
        """)
    user_manager.create(message.chat.id, message.from_user.id, )


@bot.message_handler(commands=('add',))
def handle_add(message: Message) -> None:
    bot.send_message(message.chat.id, text="Send me a message with the card question followed by a "
                                           "message with the answer.")
    user_manager.setUserState(chat_id=message.chat.id,
                              user_id=message.from_user.id,
                              state=UserManager.ADD_CARD_QUESTION)


@bot.message_handler(commands=('learn',))
def handle_learn(message: Message) -> None:
    top_question = card_manager.current_top_for(chat_id=message.chat.id)['question']
    bot.send_message(chat_id=message.chat.id, text="Card question", reply_markup=markup_question)
    bot.forward_message(chat_id=message.chat.id, from_chat_id=top_question['from_chat_id'],
                        message_id=top_question['message_id'])


@bot.message_handler(commands=('show',))
def sendAnswer(message):
    top_answer = card_manager.current_top_for(chat_id=message.chat.id)['answer']
    bot.send_message(chat_id=message.chat.id, text="Card answer", reply_markup=markup_pull)
    bot.forward_message(chat_id=message.chat.id, from_chat_id=top_answer['from_chat_id'],
                        message_id=top_answer['message_id'])


@bot.message_handler(commands=('hard',))
def handle_forgot(message: Message) -> None:
    card_manager.update_level(card_manager.current_top_for(chat_id=message.chat.id), -1)
    handle_learn(message)


@bot.message_handler(commands=('good',))
def handle_remember(message: Message) -> None:
    card_manager.update_level(card_manager.current_top_for(chat_id=message.chat.id), 1)
    handle_learn(message)


@bot.message_handler(content_types=('text', 'photo', 'audio', 'document'))
def handle_basic_message(message: Message) -> None:
    user_state = user_manager.getUser(chat_id=message.chat.id, user_id=message.from_user.id)['state']
    if user_state == user_manager.LEARNING_STATE:
        return

    if user_state == user_manager.ADD_CARD_QUESTION:
        user_manager.setUserState(message.chat.id, message.from_user.id, user_manager.ADD_CARD_ANSWER)
        user_manager.saveQuestion(message)
        bot.send_message(chat_id=message.chat.id, text='Got it. Now send me the answer.')

    if user_state == user_manager.ADD_CARD_ANSWER:
        card_manager.add(chat_id=message.chat.id,
                         question=user_manager.getSavedQuestion(message),
                         answer={'chat': {'id': message.chat.id}, 'message_id': message.message_id})
        user_manager.setUserState(message.chat.id, message.from_user.id, user_manager.LEARNING_STATE)
        handle_learn(message)


if __name__ == '__main__':
    bot.polling()
