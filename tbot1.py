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
        'Вы хотите большую пиццу, оплата - наличкой?',
        'Вы хотите большую пиццу, оплата - картой?',
        'Вы хотите маленькую пиццу, оплата - наличкой?',
        'Вы хотите маленькую пиццу, оплата - картой?',
        'Спасибо за заказ. Закажете еще одну пиццу?',
        'Попробуете еще раз? (да/нет)',
        'Какую вы хотите пиццу? Большую или маленькую?',
        'Для заказа пиццы напечатайте "/start"',
        'До свидания'
        ]

transitions = [
    { 'trigger': '*', 
      'source': '*', 
      'dest': 'Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?' },

    { 'trigger': 'большую', 
      'source': 'Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?', 
      'dest': 'Как вы будете платить? Наличкой или картой?' },

    { 'trigger': 'маленькую', 
      'source': 'Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?', 
      'dest': 'Как вы будете платить? Картой или наличкой?' },

      { 'trigger': 'большую', 
      'source': 'Какую вы хотите пиццу? Большую или маленькую?', 
      'dest': 'Как вы будете платить? Наличкой или картой?' },

    { 'trigger': 'маленькую', 
      'source': 'Какую вы хотите пиццу? Большую или маленькую?', 
      'dest': 'Как вы будете платить? Картой или наличкой?' },

    { 'trigger': 'наличкой', 
      'source': 'Как вы будете платить? Наличкой или картой?', 
      'dest': 'Вы хотите большую пиццу, оплата - наличкой?' },

    { 'trigger': 'картой', 
      'source': 'Как вы будете платить? Наличкой или картой?', 
      'dest': 'Вы хотите большую пиццу, оплата - картой?' },  

    { 'trigger': 'наличкой', 
      'source': 'Как вы будете платить? Картой или наличкой?', 
      'dest': 'Вы хотите маленькую пиццу, оплата - наличкой?' },

    { 'trigger': 'картой', 
      'source': 'Как вы будете платить? Картой или наличкой?', 
      'dest': 'Вы хотите маленькую пиццу, оплата - картой?' },

    { 'trigger': 'да', 
      'source': 'Вы хотите маленькую пиццу, оплата - наличкой?', 
      'dest': 'Спасибо за заказ. Закажете еще одну пиццу?' },

    { 'trigger': 'да', 
      'source': 'Вы хотите маленькую пиццу, оплата - картой?', 
      'dest': 'Спасибо за заказ. Закажете еще одну пиццу?' },

    { 'trigger': 'да', 
      'source': 'Вы хотите большую пиццу, оплата - наличкой?', 
      'dest': 'Спасибо за заказ. Закажете еще одну пиццу?' },

    { 'trigger': 'да', 
      'source': 'Вы хотите большую пиццу, оплата - картой?', 
      'dest': 'Спасибо за заказ. Закажете еще одну пиццу?' },

    { 'trigger': 'нет', 
      'source': 'Вы хотите маленькую пиццу, оплата - наличкой?', 
      'dest': 'Попробуете еще раз? (да/нет)' },

    { 'trigger': 'нет', 
      'source': 'Вы хотите маленькую пиццу, оплата - картой?', 
      'dest': 'Попробуете еще раз? (да/нет)' },

    { 'trigger': 'нет', 
      'source': 'Вы хотите большую пиццу, оплата - наличкой?', 
      'dest': 'Попробуете еще раз? (да/нет)' },

    { 'trigger': 'нет', 
      'source': 'Вы хотите большую пиццу, оплата - картой?', 
      'dest': 'Попробуете еще раз? (да/нет)' },

    { 'trigger': 'да', 
      'source': 'Спасибо за заказ. Закажете еще одну пиццу?', 
      'dest': 'Какую вы хотите пиццу? Большую или маленькую?' },

    { 'trigger': 'нет', 
      'source': 'Спасибо за заказ. Закажете еще одну пиццу?', 
      'dest': 'До свидания' },

    { 'trigger': 'да', 
      'source': 'Попробуете еще раз? (да/нет)', 
      'dest': 'Какую вы хотите пиццу? Большую или маленькую?' },

    { 'trigger': 'нет', 
      'source': 'Попробуете еще раз? (да/нет)', 
      'dest': 'До свидания' },

    { 'trigger': 'До свидания', 
      'source': 'До свидания', 
      'dest': 'Для заказа пиццы напечатайте "/start"' },
]

machine = Machine(lump, states=states, transitions=transitions, 
	              initial='Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?')

# функция обработки команды '/start'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Здравствуйте! Какую вы хотите пиццу? Большую или маленькую?")

# функция обработки текстовых сообщений
def message(update, context):
    try:
        lump.trigger(update.message.text.lower())
    except Exception as e:
        print(e)
    text = lump.state
    if text == 'До свидания':
    	lump.trigger(text)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text) 

# функция обработки не распознных команд
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Извините, я не понял эту команду")

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
