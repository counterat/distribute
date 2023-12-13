import asyncio
import logging
import random
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
from spotify_module_for_bot import search_tracks_in_spotify, download_video_from_yt, download_video_from_yt_by_link, get_audio_link_from_video
from main import get_members_of_chat_for_spotify_bot, app
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Boolean, ForeignKey,ARRAY, Table, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
API_TOKEN = '6869452549:AAEN0_bPbvvi09eKTzHYZtzMEczrxKBk9rM'
# API_TOKEN = '6871959789:AAGJH-9tfLmNm22Ty-IVId9XFcDFkqHjohk'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


Base = declarative_base()



class Music(Base):
    title = Column(String, primary_key=True)
    audio_id = Column(String)
    __tablename__ = 'songs'

class UsersOfSpotifyBotDatabase(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    username = Column(String)
    num_of_tries = Column(Integer, default=0)
    is_pro = Column(Integer, default=0)
    __tablename__ = 'UsersOfSpotifyBotDatabase'

engine = create_engine('sqlite:///mydatabase_for_music.db')


Base.metadata.create_all(engine)
# Создаем сессию SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()


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

        if user_id in  await get_members_of_chat_for_spotify_bot(chat_id) and user_id in await get_members_of_chat_for_spotify_bot(-1002003664829):
            return True
        return False
@dp.inline_handler(lambda query: True)
async def inline_query(query: types.InlineQuery):


        results = []
        if len(query.query) >5:
            tracks = search_tracks_in_spotify(query.query, 1)

            for track in tracks:
                tracks_in_dbb = session.query(Music).all()
                tracks_in_db = []
                for title in tracks_in_dbb:
                    tracks_in_db.append(title.title)
                result_string = ''.join(char for char in track if char.isalpha())
                if result_string not in tracks_in_db:
                    results.append(
                        types.InlineQueryResultArticle(
                            id=f'1',

                            title='Песни пока нету в базе, попробуйте через 10 секунд',

                            input_message_content=types.InputTextMessageContent(
                                message_text=f'Песни пока нету в базе, попробуйте через 10 секунд')

                            # Укажите длительность аудио в секундах
                        )

                    )
                    await bot.answer_inline_query(query.id, results,switch_pm_text='Попробуй здесь',
    switch_pm_parameter=f'pm_param_{random.randint(1, 100)}', cache_time=1)
                    print(track)
                    print(tracks_in_db)

                    await bot.send_message(6735763833, f'{query.from_user.id}, {os.path.exists(str(query.from_user.id))} ')
                    if not (os.path.exists(f'{query.from_user.id}')):
                        os.mkdir(f'{query.from_user.id}')
                    download_video_from_yt(track, query.from_user.id)


                    with open(f'{query.from_user.id}/{track}.mp4', 'rb') as audio:
                        infoaudio =await bot.send_audio(chat_id=6735763833, audio=audio, title=f'{track}')
                        # Получение информации о переданном аудио
                        audio_info = infoaudio.audio

                        # Теперь вы можете извлечь название аудио
                        audio_title = audio_info.file_name

                        try:
                            new_track = Music(title=result_string, audio_id = infoaudio.audio.file_id)
                            session.add(new_track)
                            session.commit()

                            os.remove(f'{query.from_user.id}/{track}.mp4')
                        except Exception as ex:
                            print(ex)
                            session.rollback()
                    print(infoaudio.audio.file_id)



                else:

                    track = session.query(Music).filter(Music.title == result_string).first()

                    results.append(
                        types.InlineQueryResultCachedAudio(
                            id=f'1',

                            caption= '@newspotifysavebot',
                            audio_file_id=track.audio_id,



                            # Укажите длительность аудио в секундах
                        )

                    )

                    await bot.answer_inline_query(query.id, results)
            # Отправляем ответ на инлайн-квери'




@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('pressed'))
async def track_callback_handler(query:types.CallbackQuery):
    if not await is_in_the_chat(query.from_user.id):
        await query.message.answer('''
*Чтобы пользоваться ботом подпишись на эти два канала
@yuraroadmap
@newspotifysavebotchannel*

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
Я помогу найти аудио аудио в Spotify и по возможности отправлю тебе его!

• Введи *автора*, или *название трека* и я покажу результаты по запросу!
• Также поддерживаю ссылки на видео с YouTube и другие популярные стриминговые сервисы
• Я ищу только оригиналы треков, без фанатских ремиксов и записи с диктофона!
• Формат треков — M4A AAC 128 Kbps. Это оригинальный формат аудио на YouTube. (!) 
• Можешь вызвать меня в *любом чате* просто напиши @newspotifysavebot
    
    
    ''', parse_mode=ParseMode.MARKDOWN)
    if not (os.path.exists(f'{message.from_user.id}')):
        os.mkdir(f'{message.from_user.id}')


    if not session.query(UsersOfSpotifyBotDatabase).filter(UsersOfSpotifyBotDatabase.id == message.from_user.id).first():
        username = None
        if message.from_user.username:
            username = message.from_user.username
        new_user = UsersOfSpotifyBotDatabase(id = message.from_user.id, first_name = message.from_user.first_name, username = username)
        session.add(new_user)
        session.commit()



@dp.message_handler(lambda message: message.text.startswith('https://www.youtube.com/watch?v='))
async  def yt_links_handler(message:types.Message):
    if not await is_in_the_chat(message.from_user.id):
        await message.answer('''
*Чтобы пользоваться ботом подпишись на эти два канала
@yuraroadmap
@newspotifysavebotchannel*

                ''', parse_mode=ParseMode.MARKDOWN)
        return
    try:
        title = download_video_from_yt_by_link(message.text, message.from_user.id)
        with open(f'{message.from_user.id}/{title}.mp4', 'rb') as file:
            await bot.send_audio(message.from_user.id, audio=InputFile(file),caption='''@newspotifysavebot''' )

        os.remove(f'{message.from_user.id}/{title}.mp4')
    except Exception as ex:
        print(ex)

@dp.message_handler()
async def handle_title_of_tracks(message: types.Message):
    user = session.query(UsersOfSpotifyBotDatabase).filter(UsersOfSpotifyBotDatabase.id == message.from_user.id).first()
    user.num_of_tries += 1
    session.commit()
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
