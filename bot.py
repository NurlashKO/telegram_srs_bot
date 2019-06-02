from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from storages.mongo import CardManager
from storages.sanitizers import question_and_answer_from


def set_up_bot() -> TeleBot:
    return TeleBot('849639836:AAETYUnkEBESn6EfQcxjgcC_l4c_kBDFcMY')


def set_up_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2)
    forgot_response = KeyboardButton('/hard')
    remember_response = KeyboardButton('/good')
    markup.add(forgot_response, remember_response)
    return markup


bot = set_up_bot()
markup = set_up_markup()
card_manager = CardManager()


@bot.message_handler(commands=('start', 'help',))
def send_welcome(message: Message):
    bot.reply_to(message, """Hey, I am here to help you with memorizing stuff.
Add your words using the following command:
    /add `Question` -/- `Answer`
    
Example:
    /add 日本語　-/- Japanese Language
    
    
To get back to your reviews use command:
    /review
    
HF ;)
    """)


@bot.message_handler(commands=('add',))
def handle_add(message: Message) -> None:
    try:
        question, answer = question_and_answer_from(message=message)
        card_manager.add(chat_id=message.chat.id, question=question, answer=answer)
        replying_message = f'Added.\n\nQuestion:\n{question}\n\nAnswer:\n{answer}'
        bot.send_message(message.chat.id, text=replying_message)
    except ValueError as err:
        bot.reply_to(message, err)


@bot.message_handler(commands=('learn',))
def handle_learn(message: Message) -> None:
    top_question = card_manager.current_top_for(chat_id=message.chat.id)['question']
    bot.send_message(chat_id=message.chat.id, text=top_question, reply_markup=markup)


@bot.message_handler(commands=('hard',))
def handle_forgot(message: Message) -> None:
    card_manager.update_level(card_manager.current_top_for(chat_id=message.chat.id), -1)
    handle_learn(message)


@bot.message_handler(commands=('good',))
def handle_remember(message: Message) -> None:
    card_manager.update_level(card_manager.current_top_for(chat_id=message.chat.id), 1)
    handle_learn(message)


if __name__ == '__main__':
    bot.polling()
