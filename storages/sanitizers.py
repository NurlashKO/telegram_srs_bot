def question_and_answer_from(message):
    print(type(message))
    data = message.text.split(' ', 1)[1]
    return data.split('-/-')
