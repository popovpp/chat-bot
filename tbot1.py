from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler
from transitions import Machine




TOKEN = '2117156469:AAEjvdiPQj32FT20YOCVJ1kIgyzUAZubIRs'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# State-machine
class Matter(object):
    pass

lump = Matter()

states=['Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?', 
        'Как вы будете платить? Наличкой или картой?', 
        'Как вы будете платить? Картой или наличкой?',
        'Вы хотите большую пиццу, оплата - наличкой? (да/нет)',
        'Вы хотите большую пиццу, оплата - картой? (да/нет)',
        'Вы хотите маленькую пиццу, оплата - наличкой? (да/нет)',
        'Вы хотите маленькую пиццу, оплата - картой? (да/нет)',
        'Спасибо за заказ. Закажете еще одну пиццу? (да/нет)',
        'Попробуете еще раз? (да/нет)',
        'Какую вы хотите пиццу? Большую или маленькую?',
        'Для заказа пиццы напечатайте "/start"',
        'До свидания'
        ]

transitions = [
    { 'trigger': '*', 
      'source': '*', 
      'dest': states[0] },

    { 'trigger': 'большую', 
      'source': states[0], 
      'dest': states[1] },

    { 'trigger': 'маленькую', 
      'source': states[0], 
      'dest': states[2] },

    { 'trigger': 'большую', 
      'source': states[9], 
      'dest': states[1] },

    { 'trigger': 'маленькую', 
      'source': states[9], 
      'dest': states[2] },

    { 'trigger': 'наличкой', 
      'source': states[1], 
      'dest': states[3] },

    { 'trigger': 'картой', 
      'source': states[1], 
      'dest': states[4] },  

    { 'trigger': 'наличкой', 
      'source': states[2], 
      'dest': states[5] },

    { 'trigger': 'картой', 
      'source': states[2], 
      'dest': states[6] },

    { 'trigger': 'да', 
      'source': states[5], 
      'dest': states[7] },

    { 'trigger': 'да', 
      'source': states[6], 
      'dest': states[7] },

    { 'trigger': 'да', 
      'source': states[3], 
      'dest': states[7] },

    { 'trigger': 'да', 
      'source': states[4], 
      'dest': states[7] },

    { 'trigger': 'нет', 
      'source': states[5], 
      'dest': states[8] },

    { 'trigger': 'нет', 
      'source': states[6], 
      'dest': states[8] },

    { 'trigger': 'нет', 
      'source': states[3], 
      'dest': states[8] },

    { 'trigger': 'нет', 
      'source': states[4], 
      'dest': states[8] },

    { 'trigger': 'да', 
      'source': states[7], 
      'dest': states[9] },

    { 'trigger': 'нет', 
      'source': states[7], 
      'dest': states[11] },

    { 'trigger': 'да', 
      'source': states[8], 
      'dest': states[9] },

    { 'trigger': 'нет', 
      'source': states[8], 
      'dest': states[11] },

    { 'trigger': states[11], 
      'source': states[11], 
      'dest': states[10] },

    { 'trigger': '/start', 
      'source': states[10], 
      'dest': states[0] }
]

machine = Machine(lump, states=states, transitions=transitions, 
                  initial=states[0])

# функция обработки команды '/start'
def start(update, context):
    try:
        lump.trigger(update.message.text.lower())
    except Exception as e:
        print(e)
    text = lump.state
    context.bot.send_message(chat_id=update.effective_chat.id, 
    	                     text=text)

# функция обработки текстовых сообщений
def message(update, context):
    try:
        lump.trigger(update.message.text.lower())
    except Exception as e:
        print(e)
    text = lump.state
    if text == states[11]:
        lump.trigger(text)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text) 

# функция обработки не распознных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Извините, я не понял эту команду")

if __name__ == '__main__':

    # обработчик команды '/start'
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)    

    # обработчик текстовых сообщений
    message_handler = MessageHandler(Filters.text & (~Filters.command), message)
    dispatcher.add_handler(message_handler)

    # обработчик не распознных команд
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # запуск прослушивания сообщений
    updater.start_polling()
    # обработчик нажатия Ctrl+C
    updater.idle()
