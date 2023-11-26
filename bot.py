import asyncio
import logging
from datetime import timedelta, datetime
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InputFile, InputMedia, InputMediaPhoto, \
    CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '6791788764:AAGdriyeyJTSg3m5GBcjxBtMKHz31ynP9WQ'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
def reply_kb_for_start(query = None):
    if query:
        return InlineKeyboardMarkup().add(InlineKeyboardButton('Связаться', url = 'https://t.me/yuriy_bsrb'))
    keyboard_for_start = InlineKeyboardMarkup()
    keyboard_for_start.add(InlineKeyboardButton('СКАМ Бот', callback_data='scam_bot'))
    keyboard_for_start.add(InlineKeyboardButton('Рассылка Телеграм', callback_data='distribution_telegram'))
    keyboard_for_start.add(InlineKeyboardButton('База данных из чатов', callback_data='database_of_chats'))
    return keyboard_for_start

class StartStates(StatesGroup):
    first = State()

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'start')
async def turn_start_state(query:types.CallbackQuery):
    await StartStates.first.set()

@dp.message_handler((Command("start") | CallbackQuery(pattern="^start$") ))
async def start_handler(message:types.Message):

    template = '''
**Привет🔥**
**МЫ - ЛУЧШАЯ команда разработчиков Telegram БОТОВ**

**🤑Наши услуги🤑**

**🥇Написание СКАМ ботов🤖💻**
__Написание клонов известных воркинг🦣 ботов, по типу R.G.T и т.д__
__Написание уникальных☝️ботов__
__Корректировка✅ ботов__
__Допиливание функций🛠️ в уже имеющихся ботах__

**В настоящий момент имеются 4 бота для продажи🛒**

__Трейдинг бот💹__
__Эскорт бот👠🔞__
__Админ панель🕹️__
__Бот для выплат воркерам💰__

**🥈Рассылка рекламы по более 500 чатам Telegram📢💌**
__БАЗА ИЗ БОЛЕЕ__ **500** __ЧАТОВ РАЗДЕЛЕННАЯ НА__ **10** __КАТЕГОРИЙ__
**ТАРГЕТТИРОВАНАЯ РЕКЛАМА** __ДЛЯ ВАШЕГО__ **БИЗНЕСА**

**🥉 📊Продажа баз данных💾 с телеграм чатами🗨️**
**База данных состоит из:**
__Ссылки на чат__
__Категория, к которой относится чат__
__Регион, в котором находится чат__
__Количество участников__
__Телеграм ID чата__

**Нажмите на кнопках ниже что вас интересует**    
'''
    with open('photo/Yellow Cryptocurrency Your Story.png', 'rb') as image:
        await message.answer_photo(photo= InputFile(image), caption=template.replace('**', '*').replace('__', '_'), parse_mode=ParseMode.MARKDOWN,
                                                          reply_markup=reply_kb_for_start())
    await message.delete()
@dp.callback_query_handler(lambda callback_query: callback_query.data in ['scam_bot','distribution_telegram', 'database_of_chats' ])
async def callback_query_handler_of_start_reply_kb(query: types.CallbackQuery):
    if query.data == 'scam_bot':
        template = '''

**🥇Написание СКАМ ботов🤖💻**
__Написание клонов известных воркинг🦣 ботов, по типу R.G.T и т.д__
__Написание уникальных☝️ботов__
__Корректировка✅ ботов__
__Допиливание функций🛠️ в уже имеющихся ботах__

**В настоящий момент имеются 4 бота для продажи🛒**

__Трейдинг бот💹__
__Эскорт бот👠🔞__
__Админ панель🕹️__
__Бот для выплат воркерам💰__
        
**Все 4 бота являются идентичной копией ботов @RGT_workbot с улучшенным функционалом**

**Изменения: **
__ОПЛАТА с помощью КРИПТОВАЛЮТЫ реализована через сервис CRYPTOMUS__
__Маммонту НЕ НАДО переходить в другой БОТ чтобы связаться с ТЕХ.ПОДДЕРЖКОЙ__
__ВЫ можете ПОДТВЕРДИТЬ или ОТКЛОНИТЬ запрос на вывод средств со счёта ВОРКЕРА через БОТА__
__ВОЗМОЖНОСТЬ подкручивать УДАЧУ МАММОНТАМ__
**ВСЕ ДЕНЬГИ ИДУТ ТОЛЬКО ВАМ И ВОРКЕРУ**
**НИКАКИХ КОМИССИЙ**

**ПРАЙС**
*100$ за все 4 БОТА*
*Написть новый бот и другие услуги - ДОГОВОРНАЯ ЦЕНА*
*Мы ГОТОВЫ на оплату через ГАРАНТА с ВАШЕЙ стороны*
*Оплата криптой или на карту*
        '''.replace('__','_').replace('**','*')
        with open('photo/photo_2023-07-04_21-05-47.jpg', 'rb') as image:
            await query.message.edit_media(InputMediaPhoto(image))
        await query.message.edit_reply_markup(reply_markup=reply_kb_for_start(query.data))
        await query.message.edit_caption(template, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_kb_for_start(query.data))


    elif query.data == 'distribution_telegram':
        template = '''
🥈Рассылка рекламы по более 500 чатам Telegram📢💌
БАЗА ИЗ БОЛЕЕ 500 ЧАТОВ РАЗДЕЛЕННАЯ НА 10 КАТЕГОРИЙ
ТАРГЕТТИРОВАНАЯ РЕКЛАМА ДЛЯ ВАШЕГО БИЗНЕСА

🔔Рекламируем:
🔺Каналы
🔺Объявления о работе
🔺Реферальные ссылки
🔺Боты
🔺Сайты
И многое другое!

**🔥Огромный приход!
🔥Классное оформление вашего постa, советы от настоящих профи!**


Если без корректировки по боту то след прайс:

**10 КАТЕГОРИЙ**
__🎙Пиар и Реклама📺
🏋️Фитнесс и здоровье🧖
👩‍❤️‍💋‍👨Общение (чаты знакомств, чаты по интересам и т.д)💌
🏬Торговые площадки, Барахолки, КуплюПродам🛒
🛠Поиск работы, объявления о работе💻
💃Мода и одежда👠
⛹️‍♀️Спорт, ставки на спорт⚽️
💱Крипта и все что с ней связано :)💹__

**1 КАТЕГОРИЯ = 1$**

__📚12 часов paccылки - 5$
📚1 День paccылки - 7$
📚3 Дня paccылки - 18$
📚7 Дней paccылки + ПРЕМИУМ(РАССЫЛКА ПО ЛС) - 60$__

__⚠️За создание уникального текста дополнительно взимается плата в размере 3$__

🆓Первые 3 корректировки - **бесплатно**
*Мы ГОТОВЫ на оплату через ГАРАНТА с ВАШЕЙ стороны*
*Оплата криптой или на карту*
        '''.replace('__','_').replace('**','*')
        with open('photo/для рассылки.png', 'rb') as image:
            await query.message.edit_media(InputMediaPhoto(image))
        await query.message.edit_caption(template, parse_mode=ParseMode.MARKDOWN,reply_markup=InlineKeyboardMarkup(InlineKeyboardButton('Связаться', url='https://t.me/yuriy_bsrb')))
        await query.message.edit_reply_markup(reply_markup=reply_kb_for_start(query.data))

    else:
        template = '''
**🥉 📊Продажа баз данных💾 с телеграм чатами🗨️
База данных состоит из:**
__Ссылки на чат
Категория, к которой относится чат
Регион, в котором находится чат
Количество участников
Телеграм ID чата__        
        
**ПРАЙС**
__за каждые 100 чатов по СНГ - 1$__
__за каждые 100 чатов по западу - 2$__
*Мы ГОТОВЫ на оплату через ГАРАНТА с ВАШЕЙ стороны*
*Оплата криптой или на карту*
        '''.replace('__','_').replace('**','*')
        with open('photo/Без названия (6).jfif', 'rb') as image:
            await query.message.edit_media(InputMediaPhoto(image))
        await query.message.edit_caption(template, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(InlineKeyboardButton('Связаться', url='https://t.me/yuriy_bsrb')))
        await query.message.edit_reply_markup(reply_markup=reply_kb_for_start(query.data))


if __name__ == '__main__':

    from aiogram import executor
    import threading



    storage = MemoryStorage()
    # Подключаем MemoryStorage к боту
    dp.storage = storage
    executor.start_polling(dp, skip_updates=True)