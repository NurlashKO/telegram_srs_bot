import telebot
from telebot import types

from actions import add_card, current_top, guess_correct, guess_wrong

bot = telebot.TeleBot('849639836:AAETYUnkEBESn6EfQcxjgcC_l4c_kBDFcMY')
markup = types.ReplyKeyboardMarkup(row_width=2)
forgot_response = types.KeyboardButton('/hard')
remember_response = types.KeyboardButton('/good')
markup.add(forgot_response, remember_response)


@bot.message_handler(commands=('start', 'help',))
def send_welcome(message):
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
def handle_add(message):
    clear_message = message.text.split(' ', 1)[1]
    try:
        question, answer = add_card(message.chat.id, clear_message)
        bot.send_message(message.chat.id, "Added.\n\nQuestion:\n{}\n\nAnswer:\n{}".format(question, answer))
    except ValueError as err:
        bot.reply_to(message, err)


@bot.message_handler(commands=('learn',))
def handle_learn(message):
    top_question = current_top()["question"]
    bot.send_message(chat_id=message.chat.id, text=top_question, reply_markup=markup)


@bot.message_handler(commands=('hard',))
def handle_forgot(message):
    guess_wrong(current_top())
    handle_learn(message)


@bot.message_handler(commands=('good',))
def handle_remember(message):
    guess_correct(current_top())
    handle_learn(message)


if __name__ == '__main__':
    bot.polling()
