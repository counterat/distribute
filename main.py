from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from config import api_id, api_hash, api_hash_for_gorilla, api_id_for_gorilla
import asyncio
import logging
import time
import asyncio
import threading
logging.basicConfig(level=logging.INFO)
app = Client('my_account_gorilla', api_id=api_id_for_gorilla, api_hash=api_hash_for_gorilla)

chat_id = 6032759612
ids = set()
async def send_message():
    while True:
        await app.send_message(chat_id, "Ебать зацени рассылку")
        await asyncio.sleep(0.25)

async def process_favorite_messages():
    # Получаем избранные сообщения


    # Проходимся по каждому сообщению
    async for message in app.get_chat_history(chat_id=chat_id):

        id = (f"Text: {message.text.split('id: -')[1].split('Text:')[0]}")
        id = (-int(id.replace('Text: ', '')))
        ids.add(id)


async def process_sergey():

    async for message in app.get_chat_history(chat_id=782266258):
        try:
            id = message.text.split('id: -')[1]
            id = -int(id)
            ids.add(id)
        except:
            'ok'
def get_members_of_chat(chat_id, quantity=50):
    members = []
    with app:
        for message in (app.get_chat_history(chat_id)):
            if len(members)>quantity:
                break
            members.append(message.from_user.id)
        return members

async def distribute_black_cats():

    while True:
        try:
            template = '''
**😩ЗАЕБАЛСЯ СИДЕТЬ БЕЗ ДЕНЕГ?😩

💵💸💲ХОЧЕШЬ ЗАРАБОТАТЬ БЕЗ ВЛОЖЕНИЙ НЕ ВЫХОДЯ ИЗ ДОМА?💲💸💵

ТЕБЕ КО МНЕ😏

🤥🦣САМЫЙ ДЕШЕВЫЙ БОТ ДЛЯ СКАМА МАММОНТОВ🦣🤥

РАБОТАЕТ ПО ВСЕМУ СНГ🇷🇺🇺🇦🇰🇿🇧🇾🇲🇩🇺🇿🇹🇲🇰🇬🇹🇯

БОТ🤖 ВКЛЮЧАЕТ В СЕБЯ АДМИН ПАНЕЛЬ⌨️, ТРЕЙДИНГ БОТА💱💹, ЭСКОРТ БОТА💦🔞 и БОТА ДЛЯ ВЫПЛАТ

УСПЕЙ ЗАКАЗАТЬ ПО СКИДОЧНОЙ ЦЕНЕ**

__1 месяц - 100$
3 месяца - 250$
неограниченное время - 500$

ПИШИ В ЛС⬇__️
||@Karina_PR_manager||
    '''
            await app.send_message(chat_id=-1001348448051, text=template, parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(60)
        except Exception as ex:
            print(ex)


async def distribute_other_chats(ids_of_chats):
    while True:

        template = '''
**📬PACCЫЛKA ВAШEГО ОБЬЯВЛЕНИЯ ПО 700 ЧAТАМ КAЖДУЮ МИНУTУ**

__📚12 часов paccылки - 5$
📚1 День paccылки - 7$
📚3 Дня paccылки - 18$
📚7 Дней paccылки + ПРЕМИУМ(РАССЫЛКА ПО ЛС) - 60$__

**🔔Рекламируем:**
`🔺Каналы
🔺Объявления о работе
🔺Реферальные ссылки
🔺Боты
🔺Сайты`
**И многое другое!**

**🔥Огромный приход!
🔥Классное оформление вашего постa, советы от настоящих профи!

🔻По поводу рассылки сюда:**
||@Karina_PR_manager||
    '''
        for id_of_chat in ids_of_chats:
            try:
                await app.send_message(chat_id=id_of_chat, text=template, parse_mode=ParseMode.MARKDOWN)
            except Exception as ex:
                print(ex)
            await asyncio.sleep(10)

async def main(ids):
    # Запускаем две асинхронные функции в бесконечном цикле
    await asyncio.gather(distribute_other_chats(ids), distribute_black_cats())

if __name__ == "__main__":
    with app:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_sergey())
        loop.run_until_complete(process_favorite_messages())
        ids = list(ids)
        loop.run_until_complete(main(ids))




