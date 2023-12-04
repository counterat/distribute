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
import os
from spotify_module_for_bot import search_tracks_in_spotify, download_video_from_yt
from main import get_members_of_chat_for_spotify_bot, app
API_TOKEN = '6869452549:AAF0wTV68F_XXClkpqADyORF9F1jbkWIiLc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)



def show_track_list(track_list:list, offset:int, limit:int):
    markup = InlineKeyboardMarkup()
    for track in track_list[offset : limit-1]:
        markup.add(InlineKeyboardButton(track, callback_data=f'pressed_{track_list.index(track)}' ))

    print(markup)
    return markup

class SendAudio(StatesGroup):
    first = State()

chat_id = -1001904060537
async def is_in_the_chat(user_id):

        if user_id in  await get_members_of_chat_for_spotify_bot(chat_id):
            return True
        return False


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('pressed'))
async def track_callback_handler(query:types.CallbackQuery):
    if not await is_in_the_chat(query.from_user.id):
        await query.message.answer('''
        *Чтобы пользоваться ботом подпишись на этот канал - @yuraroadmap*

                ''', parse_mode=ParseMode.MARKDOWN)
        return
    await bot.answer_callback_query(query.id, text="Запрос успешно обработан!")

    for key in (query.message.values['reply_markup']['inline_keyboard']):
        if query.data == (key[0]["callback_data"]):
            key[0]["callback_data"] = 'processed'
            track = key[0]['text']
            audio = download_video_from_yt(track, query.from_user.id)
            with open(f'{query.from_user.id}/{track}.mp4', 'rb') as file:
                await bot.send_audio(query.from_user.id, InputFile(file), caption='''@newspotifysavebot''')
            os.remove(f'{query.from_user.id}/{track}.mp4')

            return



@dp.message_handler(commands=['start'])
async def start_handler(message:types.Message):

    await message.answer(f'''
Привет, *{message.from_user.first_name}*! 🤚
Я помогу найти аудио аудио в YouTube Music и по возможности отправлю тебе его!

• Введи *автора*, или *название трека* и я покажу результаты по запросу!
• Также поддерживаю ссылки на видео с YouTube и другие популярные стриминговые сервисы, такие как Spotify, Apple Music, Deezer, Yandex.Music и другие.
• Я ищу только оригиналы треков, без фанатских ремиксов и записи с диктофона!
• Формат треков — M4A AAC 128 Kbps. Это оригинальный формат аудио на YouTube. (!) 
• Обложки альбомов прилагаются!
    
    
    ''', parse_mode=ParseMode.MARKDOWN)
    if not (os.path.exists('{message.from_user.id}')):
        os.mkdir(f'{message.from_user.id}')

@dp.message_handler()
async def handle_title_of_tracks(message: types.Message):
    if await is_in_the_chat(message.from_user.id):

        list_of_tracks = search_tracks_in_spotify(message.text)

        await message.answer(f'''
Мы нашли следующие треки:
Нажмите на кнопки ниже чтобы бот отправил вам эту песню!
''', reply_markup=show_track_list(list_of_tracks, offset=0, limit=11))
    else:
        await message.answer('''
*Чтобы пользоваться ботом подпишись на этот канал - @yuraroadmap*
        
        ''', parse_mode=ParseMode.MARKDOWN)



if __name__ == '__main__':

    from aiogram import executor
    import threading



    storage = MemoryStorage()
    # Подключаем MemoryStorage к боту
    dp.storage = storage
    with app:
        executor.start_polling(dp, skip_updates=True)
