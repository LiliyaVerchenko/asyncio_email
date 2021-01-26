import sqlite3
import asyncio
from email.message import EmailMessage
import aiosmtplib
import ssl
import aiosqlite


def get_users():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email != 'None'")
        user = cursor.fetchall()
        users = set(user)
        users_list = []
        for user in users:
            users_list.append(user)
        return users_list


async def create_message(id, name, password, email):
    message = EmailMessage()
    message["From"] = '################'
    message["To"] = email
    message["Subject"] = "Благодарность!"
    message.set_content("Уважаемый {name} !\n"
                        "Спасибо, что пользуетесь нашим сервисом объявлений.")
    return message


async def send_message(message):
    context = ssl.create_default_context()
    await aiosmtplib.send(
        message,
        hostname="smtp.yandex.ru",
        port=465,
        username='##########',
        password='##########',
        use_tls=True)


async def main():
    users_list = get_users()
    tasks = []
    for user in users_list:
        task = create_message(*user)
        tasks.append(task)
    messages = await asyncio.gather(*tasks)
    for message in messages:
        await send_message(message)


if __name__ == '__main__':
    asyncio.get_event_loop()
    asyncio.run(main(), debug=True)
