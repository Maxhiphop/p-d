import asyncio
import random
import sqlite3
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.exceptions import AiogramError


API_TOKEN = "7701579172:AAGg1eFhA4XtAl1I1m76IT9jVfwKLkuUkUQ"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подключение к базе данных SQLite
conn = sqlite3.connect("leaderboard.db")
cursor = conn.cursor()

# Создаем таблицу лидеров, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaders (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER DEFAULT 0
)
""")
conn.commit()


# Списки вопросов и действий
truths = [
"Какой твой самый большой секрет?",
    "Кого ты тайно любишь?",
    "Что самое странное ты когда-либо ел?",
    "Ты когда-нибудь говорил какое-то враньё от лица родителей?"
    "Ты когда-нибудь ссорился с людьми без весомой той причины?"
    "Каким увлечением ты хотела заниматься в детстве?"
    "Ты когда-нибудь боялся признаться в своих чувствах человеку?"
    "За твоей жизнью следил кто-то?"
    "Ты когда-нибудь врал о чём-то, чтобы понравиться человеку?"
    "С какой знаменитостью ты бы хотел поменяться на день?"
    "С кем бы ты хотел поцеловаться?"
    "Ты когда-нибудь врал своим родителям?",
    "Был ли у тебя вымышленный друг?",
    "Ты когда-нибудь списывал на экзамене?",
    "Какой твой самый неловкий момент в жизни?",
    "Кому ты завидуешь?",
    "Ты когда-нибудь врал своему лучшему другу?",
    "Если бы ты мог поменяться жизнями с кем-то на один день, кто бы это был?",
    "Что бы ты сделал, если бы стал невидимым на один день?",
    "Ты когда-нибудь подслушивал чужие разговоры?",
    "Какой самый глупый поступок ты совершал?",
    "Ты когда-нибудь нарушал закон?",
    "Какой у тебя был самый странный сон?",
    "Какой самый большой страх у тебя?",
    "Ты когда-нибудь притворялся больным, чтобы пропустить что-то важное?",
    "Если бы ты мог стереть один момент из своей жизни, что бы это было?",
    "Ты когда-нибудь подставлял кого-то?",
    "Какая самая постыдная вещь, которую ты делал ради любви?",
    "Какое самое безумное признание в любви ты получал?",
    "Что самое худшее, что ты сказал кому-то в гневе?",
    "Если бы ты мог узнать правду об одном секрете, что бы это было?",
    "Ты когда-нибудь ревновал без причины?",
    "Какое у тебя самое неловкое детское воспоминание?",
    "Ты когда-нибудь воровал что-то в магазине?",
    "Какую свою привычку ты считаешь самой странной?",
    "Что ты чаще всего гуглишь?",
    "Какой самый постыдный поступок ты совершил в школе?",
    "Ты когда-нибудь притворялся, что понимаешь тему разговора, когда на самом деле нет?",
    "Какой фильм или сериал заставил тебя плакать?",
    "Что самое смешное случалось с тобой на свидании?",
    "Ты когда-нибудь прогуливал уроки или работу?",
    "Какое у тебя самое неловкое фото?",
    "Какую песню ты слушаешь, но никому не признаешься?",
    "Ты когда-нибудь пользовался чужими вещами без разрешения?",
    "Какой твой самый необычный талант?",
    "Что самое глупое ты говорил во время важного разговора?",
    "Ты когда-нибудь фальшиво смеялся над шуткой начальника или учителя?",
    "Какая твоя худшая привычка?",
    "Ты когда-нибудь попадал в нелепые ситуации в общественном транспорте?",
    "Какой самый дорогой подарок ты получал?",
    "Ты когда-нибудь выдавал чужую работу за свою?",
    "Какой твой самый странный фетиш?",
    "Какой у тебя был самый большой конфуз на свидании?",
    "Ты когда-нибудь врала о своем возрасте?",
    "Какая самая дурацкая причина, по которой ты расставался с кем-то?",
    "Ты когда-нибудь играл в карты на раздевание?",
    "Какой у тебя был самый странный разговор в жизни?",
    "Ты когда-нибудь обманывал в настольных играх?",
    "Какой самый странный комплимент ты получал?",
    "Ты когда-нибудь отправлял сообщение не тому человеку?",
    "Какое твое самое детское увлечение?",
    "Ты когда-нибудь плакал из-за мультфильма?",
    "Какой самый странный поступок ты совершил ради любви?",
    "Ты когда-нибудь подделывал подпись родителей?",
    "Какой твой худший опыт на работе или учебе?",
    "Ты когда-нибудь следил за кем-то в соцсетях?",
    "Какой у тебя был самый смешной или нелепый страх?",
    "Ты когда-нибудь терял важную вещь и притворялся, что это не ты?",
    "Какой самый дорогой подарок ты сделал кому-то?",
    "Ты когда-нибудь пел в душе и тебя слышали?",
    "Какую знаменитость ты бы хотел поцеловать?",
    "Ты когда-нибудь делал что-то запретное на спор?",
    "Какой твой самый постыдный поступок в детстве?",
    "Ты когда-нибудь фальшиво говорил, что любишь кого-то?",
    "Какую книгу ты читал, но стесняешься признаться?",
    "Ты когда-нибудь пробовал написать любовное письмо?",
    "Какой твой самый нелепый или странный страх?",
    "Ты когда-нибудь говорил что-то неприятное о человеке, а он это услышал?",
    "Какой самый странный сон ты видел?",
    "Ты когда-нибудь пробовал взломать чей-то пароль?",
    "Какую знаменитость ты бы хотел видеть своим другом?",
    "Ты когда-нибудь пел в караоке и жалел об этом?",
    "Какой у тебя был самый большой провал в школе или на работе?",
    "Ты когда-нибудь стеснялся признаться в своих чувствах?",
    "Какое самое смешное прозвище у тебя было?",
    "Ты когда-нибудь воровал еду из чужой тарелки?",
    "Какой самый неприятный комментарий о себе ты слышал?",
    "Ты когда-нибудь пользовался чужим паролем без разрешения?",
    "Ты когда-нибудь стеснялся своей семьи?",
    "Какой у тебя был самый глупый или странный спор?",
    "Ты когда-нибудь лгал о том, что умеешь делать что-то, чтобы произвести впечатление?",
    "Какой самый странный поступок ты совершил ради веселья?",
    "Ты когда-нибудь пытался шпионить за кем-то?",
    "Какой у тебя был самый смешной случай с одеждой?",
    "Ты когда-нибудь притворялся, что не знаешь кого-то, кого на самом деле знаешь?",
    "Какую песню ты знаешь наизусть, но стесняешься признаться?",
    "Ты когда-нибудь сдавал чужую работу как свою?",
    "Ты когда-нибудь ревновал друга к другому другу?",
    "Какой у тебя был самый ужасный подарок?",
    "Ты когда-нибудь делал вид, что не видишь кого-то, чтобы не здороваться?",
    "Какой у тебя был самый забавный случай с животными?",
    "Ты когда-нибудь сбегал с вечеринки, не попрощавшись?",
    "Какой у тебя был самый неловкий случай на свидании?",
    "Ты когда-нибудь пользовался чьими-то духами или дезодорантом без разрешения?",
    "Какой самый странный вкус мороженого ты пробовал?",
    "Ты когда-нибудь пользовался чужими вещами без разрешения?",
    "Какой у тебя был самый странный или смешной страх в детстве?",
    "Ты когда-нибудь пропускал важное событие из-за лени?",
    "Какое твое самое смешное видео или фото из детства?",
    "Ты когда-нибудь танцевал в одиночестве перед зеркалом?",
    "Какой твой самый нелепый поступок на публике?",
    "Ты когда-нибудь случайно попадал в неловкие ситуации с незнакомцами?"
    # Добавьте другие вопросы...
]

dares = [
     "Съешь ложку соли без запивания водой!",
    "Сделай 10 отжиманий прямо сейчас!",
    "Изобрази курицу и походи так 30 секунд!",
    "Позвони случайному контакту и скажи, что скучаешь!",
    "Станцуй без музыки в течение 1 минуты!",
    "Съешь что-то с закрытыми глазами!",
    "Проговори весь алфавит задом наперёд!",
    "Изобрази известного персонажа, а остальные должны угадать!",
    "Напиши своему бывшему/бывшей, что скучаешь!",
    "Попробуй говорить как робот в течение 5 минут!",
    "Съешь кусочек лимона без гримасы!",
    "Изобрази пьяного человека в течение 30 секунд!",
    "Покажи своё самое смешное лицо!",
    "Изобрази любимое животное другого игрока!",
    "Съешь ложку варенья с солью!",
    "Произнеси любую скороговорку три раза подряд без ошибок!",
    "Говори голосом мультяшного персонажа 3 минуты!",
    "Съешь ложку кетчупа или майонеза!",
    "Сделай 20 приседаний подряд!",
    "Напиши сообщение своему начальнику или учителю с текстом «Вы классный!»",
    "Нарисуй лицо на своей руке и говори от его имени!",
    "Выпей стакан воды, стоя на одной ноге!",
    "Расскажи случайную историю с максимальным выражением эмоций!",
    "Сделай 10 прыжков на одной ноге!",
    "Изобрази сломанного робота в течение 1 минуты!",
    "Съешь кусочек сырого лука!",
    "Спой любую песню с набитым ртом!",
    "Проходи по комнате, как модель на подиуме!",
    "Скажи что-то смешное в стиле рэпа!",
    "Притворись, что ты супергерой, и придумай себе имя!",
    "Произнеси любую фразу в замедленной съемке!",
    "Разговаривай с кем-нибудь на выдуманном языке 3 минуты!",
    "Расскажи смешной анекдот без улыбки!",
    "Делай вид, что ты курица, пока не наступит твой следующий ход!",
    "Нарисуй на бумаге человека с закрытыми глазами!",
    "Изобрази оперного певца и спой любую песню!",
    "Сыграй на воображаемой гитаре в течение 30 секунд!",
    "Изобрази любимого супергероя!",
    "Скажи алфавит задом наперёд в течение 30 секунд!",
    "Сделай селфи с самым странным выражением лица и отправь его в чат!",
    "Изобрази пингвина, пока не наступит твой следующий ход!",
    "Придумай танец и покажи его всем!",
    "Сделай массаж плеч другому игроку!",
    "Изобрази собаку, которая хочет погулять!",
    "Спой национальный гимн как рэп!",
    "Съешь чайную ложку горчицы!",
    "Сделай макияж с закрытыми глазами!",
    "Выпей стакан воды через соломинку за 10 секунд!",
    "Съешь ложку смеси сахара, соли и перца!",
    "Говори высоким голосом 5 минут!",
    "Изобрази известного певца и спой его песню!",
    "Изобрази злого босса на совещании!",
    "Нарисуй свой портрет, используя только свою слабую руку!",
    "Покажи сцену из своего любимого фильма!",
    "Говори, вставляя после каждого слова «мяу», в течение 5 минут!",
    "Построй башню из подручных предметов за 1 минуту!",
    "Сделай 15 прыжков со звуком лягушки!",
    "Спой песню, но меняя все слова на «ля»!",
    "Изобрази знаменитого блогера или актера!",
    "Говори голосом старика 5 минут!",
    "Придумай и расскажи историю за 30 секунд!",
    "Изобрази танцующего робота!",
    "Спой детскую песню как профессиональный певец!",
    "Изобрази кошку, которая хочет поесть!",
    "Сделай комплимент каждому игроку!",
    "Придумай новую позу для сна и продемонстрируй её!",
    "Изобрази героя из любимого мультфильма!",
    "Притворись официантом и обслужи другого игрока!",
    "Нарисуй что-то пальцем в воздухе, а другие должны угадать!",
    "Изобрази едущего на мотоцикле, издавая звуки двигателя!",
    "Съешь кусочек шоколада с солёным огурцом!",
    "Изобрази человека, который попал под дождь!",
    "Сыграй в «камень, ножницы, бумага» с кем-нибудь!",
    "Скажи что-то приятное о каждом игроке!",
    "Придумай новый вид спорта и объясни его правила!",
    "Изобрази попугая, который повторяет всё подряд!",
    "Изобрази человека, который ищет потерянные очки!",
    "Спой любую песню, но с закрытым ртом!",
    "Изобрази зомби, который очень хочет кофе!",
    "Сыграй на воображаемой барабанной установке!",
    "Придумай новый язык и поговори на нем 1 минуту!",
    "Притворись радиоведущим и расскажи новости!",
    "Спой песню, но только шёпотом!",
    "Изобрази болельщика, чей любимый клуб проигрывает!",
    "Придумай новую йога-позу и назови её!",
    "Станцуй как клоун 30 секунд!",
    "Изобрази ребенка, который требует купить игрушку!",
    "Попробуй стоять на одной ноге 1 минуту!",
    "Изобрази, что ты в невидимой коробке!",
    "Покажи сцену из фильма без слов, а другие должны угадать!",
    "Придумай новую пословицу и объясни её смысл!",
    "Скажи что-то весёлое в стиле стихотворения!",
    "Изобрази себя в старости и поговори с кем-то!",
    "Сыграй в классики, нарисовав их пальцем на полу!",
    "Придумай и расскажи смешную рекламу!",
    "Сделай воздушный поцелуй каждому игроку!",
    "Попробуй поймать невидимый объект!",
    "Изобрази космонавта в невесомости!",
    "Притворись супергероем и представь свой костюм!",
    "Сделай вид, что ты сломанный робот!",
    "Произнеси 10 скороговорок подряд!",
    "Изобрази, как ты тонешь, а другие должны спасти тебя!",
    "Говори только с помощью жестов 5 минут!",
    "Придумай новое движение для танца и покажи его!",
    "Покажи, как ты бы вел себя, если бы выиграл миллион!",
    "Изобрази очень радостного пингвина!"
    # Добавьте другие действия...
]


# Словарь для антиспама
user_spam = {}

# Функция выбора случайного элемента
def get_random_item(lst):
    return random.choice(lst)

# Функция обновления таблицы лидеров
def update_leaderboard(user_id, username):
    cursor.execute("SELECT score FROM leaders WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute("UPDATE leaders SET score = score + 1 WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("INSERT INTO leaders (user_id, username, score) VALUES (?, ?, 1)", (user_id, username))
    
    conn.commit()

# Функция получения таблицы лидеров
def get_leaderboard():
    cursor.execute("SELECT username, score FROM leaders ORDER BY score DESC LIMIT 10")
    leaders = cursor.fetchall()
    
    if not leaders:
        return "Пока никто не играл!"
    
    return "\n".join([f"{i+1}. {user[0]} - {user[1]} корон" for i, user in enumerate(leaders)])

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Кнопки
    truth_button = KeyboardButton(text="Правда")
    dare_button = KeyboardButton(text="Вызов")
    leaderboard_button = KeyboardButton(text="Таблица лидеров")
    
    # Клавиатура
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[truth_button, dare_button, leaderboard_button]], 
        resize_keyboard=True
    )
    
    await message.answer("Привет! Выбери: Правда или Вызов?", reply_markup=keyboard)

# Обработка кнопок + антиспам
@dp.message(lambda message: message.text in ["Правда", "Вызов", "Таблица лидеров"])
async def handle_buttons(message: types.Message):
    user_id = message.from_user.id
    text = message.text.lower()

    # Проверка спама
    current_time = time.time()
    if user_id in user_spam:
        user_spam[user_id].append(current_time)
        user_spam[user_id] = [t for t in user_spam[user_id] if current_time - t < 5]  # Убираем старые записи

        if len(user_spam[user_id]) > 3:  # Если больше 3 сообщений за 5 секунд
            try:
                await message.bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=types.ChatPermissions(can_send_messages=False),
                    until_date=int(time.time()) + 60  # Мут на 60 секунд
                )
                await message.answer("Вы были заблокированы на 60 секунд за частые сообщения.")
            except AiogramError as e:
                await message.answer(f"Ошибка: {e}")
    
    # Обработка кнопок
    if text == "правда":
        await message.answer(random.choice(truths))
        update_leaderboard(message.from_user.id, message.from_user.username)
    elif text == "вызов":
        await message.answer(random.choice(dares))
        update_leaderboard(message.from_user.id, message.from_user.username)
    elif text == "таблица лидеров":
        leaderboard = get_leaderboard()
        await message.answer(f"🏆 Топ игроков:\n{leaderboard}")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
    file.write("# p-d\n")
import subprocess

# Инициализация репозитория
subprocess.run(["git", "init"])

# Добавление файла в репозиторий
subprocess.run(["git", "add", "README.md"])

# Создание коммита
subprocess.run(["git", "commit", "-m", "first commit"])

# Установка основной ветки
subprocess.run(["git", "branch", "-M", "main"])

# Добавление удаленного репозитория
subprocess.run(["git", "remote", "add", "origin", "https://github.com/Maxhiphop/p-d.git"])

# Отправка изменений на GitHub
subprocess.run(["git", "push", "-u", "origin", "main"])
