import telebot
from telebot import types
from actions import add_card

bot = telebot.TeleBot('849639836:AAETYUnkEBESn6EfQcxjgcC_l4c_kBDFcMY')


@bot.message_handler(commands=['start', 'help'])
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

@bot.message_handler(commands=['add'])
def handle_add(message):
    clear_message = message.text.split(' ')[1]
    try:
        question, answer = add_card(clear_message)
        bot.send_message(message.chat.id, "Added.\n\nQuestion:\n{}\n\nAnswer:\n{}".format(question, answer))
    except ValueError as err:
        bot.reply_to(message, err)


markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('v')
itembtn3 = types.KeyboardButton('d')
markup.add(itembtn1, itembtn2, itembtn3)

bot.polling()
