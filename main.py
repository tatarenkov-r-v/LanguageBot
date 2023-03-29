import telebot
import config
from googletrans import Translator
import openai

bot = telebot.TeleBot(config.tg_token)

openai.api_key = config.openai_token

def make_test(word):
    response = openai.Completion.create(
      model="text-davinci-003",
        prompt="Придумай одно задание на русском языке для изучения следующего "
               "английского слова: " + word + ". "
               "\n\nПример задания:\nКак перевести слово "
               "\"frog\"?\nВыберете правильный ответ:"
               "\n1: Лось\n2: Лягушка (правильный ответ)\n3: "
               "Краб\n4: Медведь\n\nЗадание:\nКак перевести слово"
               " \"" + word + "?",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return ("Как перевести слово <b>" + word + "</b>?" + (
        response['choices'][0]['text']))



translator = Translator(service_urls=['translate.googleapis.com'])

@bot.message_handler(commands=['vocabulary'])
def show_vocabulary(message):
    with open("vocabulary.txt", "r") as file:
        lines = file.readlines()[-10:]
    for line in reversed(lines):
        bot.send_message(message.chat.id, text=line)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    bot.send_message(message.chat.id,
                     text=translator.translate(message.text, src="en",
                                               dest="ru").text)
    bot.send_message(message.chat.id, text=make_test(message.text), parse_mode="html")

    with open("vocabulary.txt", "a") as file:
        file.write(message.text + "\n")

    test = make_test(message.text).split("\n")
    # print(test)
    for i in range(2, 6):
        if (test[i].endswith(" (правильный ответ)")):
            print(test[i][3:-19])
        else:
            print(test[i][3:])


bot.polling()
