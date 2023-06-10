import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrenciesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет!\nЧтобы начать работу введите команду боту в следующем формате:\n<<имя валюты> \
<имя валюты, в которую надо перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой нужно конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую нужно конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = 'Выберите количество конвертируемой валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = CurrenciesConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации:\n{e}")
    else:
            text = f"Цена {amount} {base} в {quote} : {new_price}"
            bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')

        answer = CurrenciesConverter.get_price(*values)


    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
            bot.reply_to(message, answer)

bot.polling()