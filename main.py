import telegram
import openai
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from os.path import exists

openai.api_key = "your_api_key"

token = "your_bot_token"
id = "your_telegram_id"
 
bot = telegram.Bot(token)

bot.send_message(chat_id=id, text="Suho's AI Chat Bot is now online!")

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

updater.start_polling()
history = ""

if (exists("history.txt")):   
    history_file = open("history.txt", "r")
    history = history_file.read()
    history_file.close()



def handler(update, context):
    global history  
    user_text_initial = update.message.text + '\n'
    user_text = history + user_text_initial

    response=openai.Completion.create(
    model="text-davinci-002",
    prompt=user_text,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    )
    ai_response = response['choices'][0]['text']
    bot.send_message(chat_id=id, text=ai_response)
    history = user_text + ai_response + '\n'
    print(history)
    history_file = open("history.txt", "w")
    history_file.write(history)
    history_file.close()
 
echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)