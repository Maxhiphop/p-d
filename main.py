from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import random
import json
import traceback

TOKEN = "7701579172:AAGg1eFhA4XtAl1I1m76IT9jVfwKLkuUkUQ"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Файл для хранения статистики
STATS_FILE = "stats.json"

def load_stats():
    try:
        with open(STATS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)

stats = load_stats()

# Списки вопросов и действий
truths = [
     "Какая твоя самая большая тайна?",
    "Если бы ты мог изменить одно событие в своей жизни, что бы это было?",
    "Какой самый неловкий момент у тебя был?",
    "Было ли у тебя влюбленность в кого-то из этой группы?",
    "Что тебя больше всего пугает?",
    "Ты когда-нибудь обманывал своего лучшего друга?",
    "Если бы тебе предложили миллион долларов, но ты должен был бы отказаться от всех друзей, ты согласился бы?",
    "Какой самый глупый поступок ты когда-либо совершал?",
    "Какая твоя самая странная привычка?",
    "Если бы ты мог стать кем угодно на один день, кто бы это был?",
    "Сколько раз в день ты проверяешь свой телефон?",
    "Есть ли у тебя любимая песня, которую ты стесняешься признаться, что любишь?",
    "Ты когда-нибудь лгал родителям?",
    "Какая вещь тебя больше всего раздражает в людях?",
    "Если бы ты мог вернуться в прошлое, что бы ты сделал по-другому?",
    "Что тебе больше всего не нравится в себе?",
    "Ты когда-нибудь обижал кого-то без причины?",
    "Что самое глупое ты когда-либо делал ради любви?",
    "Какое твое худшее качество?",
    "Ты когда-нибудь скрывал свои чувства от друзей?",
    "Что для тебя важнее: честность или дружба?",
    "Ты когда-нибудь встречал кого-то, кто тебе не нравился, но ты все равно общался с ним?",
    "Что тебя бы взбесило, если бы произошло прямо сейчас?",
    "Какие у тебя были самые большие страхи в детстве?",
    "Был ли у тебя когда-нибудь такой момент, когда ты расставался с кем-то и потом сожалел?",
    "Какая твоя самая необычная фобия?",
    "Ты когда-нибудь ревновал к другу?",
    "Что бы ты сделал, если бы стал невидимым на один день?",
    "Ты когда-нибудь брал чужие вещи без спроса?",
    "Когда ты в последний раз лгал?",
    "Какое самое странное место, в котором ты был?",
    "Тебе когда-нибудь было стыдно за свою семью?",
    "Ты когда-нибудь чувствовал, что не достоин своих успехов?",
    "Какой твой самый неловкий поступок на свидании?",
    "Ты когда-нибудь открывал чужие секреты?",
    "Ты когда-нибудь ждал подарка, но он оказался не тем, что ты ожидал?",
    "Если бы ты мог узнать правду о любом человеке, что бы ты хотел узнать?",
    "Что ты скрываешь от своих близких?",
    "Ты когда-нибудь говорил людям что-то, что на самом деле не хотел говорить?",
    "Ты когда-нибудь попал в неудобное положение из-за своей честности?",
    "Что ты считаешь своим самым большим достижением?",
    "Ты когда-нибудь поступал несправедливо по отношению к кому-то?",
    "Какие у тебя были самые неудачные попытки сделать сюрприз?",
    "Ты когда-нибудь пытался манипулировать другими людьми?",
    "Какая твоя самая большая мечта, которую ты еще не осуществил?",
    "Ты когда-нибудь вел себя иначе, чем обычно, чтобы понравиться кому-то?",
    "Есть ли у тебя тайное увлечение, о котором никто не знает?",
    "Ты когда-нибудь засыпал на важной встрече?",
    "Ты когда-нибудь терял уважение к кому-то из-за их поступков?",
    "Что бы ты сделал, если бы получил шанс встретиться с кем-то, кого ты ненавидишь?",
    "Есть ли у тебя порок, от которого ты не можешь избавиться?",
    "Когда ты последний раз злился на кого-то из-за пустяков?",
    "Ты когда-нибудь чувствовал себя некомфортно в какой-то компании?",
    "Ты когда-нибудь завидовал своему другу?",
    "Что для тебя более важное: честность или забота о чувствах других?",
    "Ты когда-нибудь лгал себе?",
    "Что самое странное ты когда-либо ел?",
    "Ты когда-нибудь врал, чтобы избежать неприятных ситуаций?",
    "Ты когда-нибудь принимал решение, которое не одобряли твои близкие?",
    "Что самое нелепое ты когда-либо говорил на собеседовании?",
    "Ты когда-нибудь что-то терял и потом сильно переживал по этому поводу?",
    "Ты когда-нибудь вмешивался в чужие отношения?",
    "Есть ли у тебя какие-то тайные желания, которые ты боишься раскрыть?",
    "Ты когда-нибудь испытывал чувство стыда за поступки других людей?",
    "Ты когда-нибудь жалел о том, что сказал что-то на спор?",
    "Был ли у тебя момент, когда ты почувствовал, что тебя не ценят?",
    "Ты когда-нибудь нарушал свои принципы ради выгоды?",
    "Ты когда-нибудь обманывал в играх?",
    "Ты когда-нибудь отказывался от чего-то важного ради забавы?",
    "Какое твоё самое сильное воспоминание из детства?",
    "Ты когда-нибудь скрывал свою радость или счастье от других людей?",
    "Ты когда-нибудь приходил в чужие отношения, даже зная, что это неправильно?",
    "Ты когда-нибудь чувствовал себя чуждым в компании?",
    "Ты когда-нибудь не мог простить себя за какую-то ошибку?",
    "Ты когда-нибудь просил прощения за что-то, чего не совершал?",
    "Ты когда-нибудь становился свидетелем какой-то несправедливости и не вмешивался?",
    "Ты когда-нибудь делал что-то неэтичное, но убеждал себя, что это правильно?",
    "Ты когда-нибудь чувствовал, что ты живешь не своей жизнью?",
    "Ты когда-нибудь пытался улучшить свои отношения с кем-то, потому что тебе было выгодно?",
    "Ты когда-нибудь был в ситуации, где честность привела к неприятным последствиям?",
    "Ты когда-нибудь завидовал успеху своего друга?",
    "Ты когда-нибудь был сильно разочарован в ком-то, кого ты любил?",
    "Ты когда-нибудь скрывал правду, чтобы не разочаровать кого-то?",
    "Ты когда-нибудь лгал, чтобы избежать наказания?",
    "Ты когда-нибудь расставался с человеком, хотя не хотел этого делать?",
    "Ты когда-нибудь чувствовал, что твою доброту воспринимают как слабость?"
    # Добавьте остальные вопросы...
]

dares = [
    "Сделай 10 приседаний прямо сейчас!",
    "Отправь голосовое сообщение с комплиментом любому участнику чата.",
    "Скажи первую фразу, которая придет в голову, и не объясняй почему.",
    "Поставь смешную аватарку на 10 минут.",
    "Прочитай вслух любую строку из книги, которую ты читаешь.",
    "Напиши 5 комплиментов случайным людям в чате.",
    "Напиши сообщение своему другу, которому давно не писал.",
    "Подними что-то тяжелое и держи в руках 1 минуту.",
    "Произнеси скороговорку 5 раз подряд.",
    "Придумай и спой пару строчек песни.",
    "Прочитай вслух стихотворение, которое ты помнишь.",
    "Напиши 5 вещей, которые ты хочешь сделать в жизни.",
    "Напиши 3 факта о себе, которые никто не знает.",
    "Придумай шутку и расскажи её вслух.",
    "Поставь любой смайлик и объясни его значение.",
    "Напиши свой самый любимый анекдот.",
    "Придумай на ходу стихотворение о чем-то случайном.",
    "Назови 5 стран, в которых ты хотел бы побывать.",
    "Назови 5 фильмов, которые тебе понравились.",
    "Скажи самые смешные вещи, которые ты слышал за последний месяц.",
    "Назови все буквы алфавита в обратном порядке.",
    "Скажи свою любимую цитату и объясни её значение.",
    "Прочитай стихотворение в стиле рэп.",
    "Сделай 10 отжиманий.",
    "Придумай и озвучь фантастическую историю.",
    "Напиши 5 вещей, которые ты всегда хочешь делать.",
    "Придумай фразу, которая тебя всегда поднимет на настроение.",
    "Перескажи свою самую смешную шутку.",
    "Разгадай загадку и объясни решение.",
    "Сделай 10 ускоренных шагов по комнате.",
    "Придумай новое слово и объясни его значение.",
    "Напиши свой любимый рецепт.",
    "Сделай дыхательную гимнастику на 2 минуты.",
    "Спой фрагмент своей любимой песни.",
    "Напиши 5 вещей, которые тебе нравятся.",
    "Назови всех своих учителей по имени.",
    "Придумай способ, как провести день в парке.",
    "Пожалуйста, представь себя супергероем и покажи своё главное суперспособность." 
    # Добавьте остальные действия...
]

# Меню команд
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Начать игру"),
        types.BotCommand(command="stop", description="Остановить игру"),
        types.BotCommand(command="stat", description="Статистика очков")
    ]
    await bot.set_my_commands(commands)

# Клавиатуры
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="🚀 Начать игру")]],
    resize_keyboard=True
)

game_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🎭 Правда"), types.KeyboardButton(text="💪 Действие")],
        [types.KeyboardButton(text="⛔ Стоп"), types.KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    try:
        logging.info("Received /start command")
        user_id = str(message.from_user.id)
        if user_id not in stats:
            stats[user_id] = {"points": 0, "in_game": False}
        await state.update_data(in_game=True)
        stats[user_id]["in_game"] = True
        save_stats(stats)
        await message.answer("Привет! Давай сыграем в 'Правду или Действие'! Выбирай:", reply_markup=game_keyboard)
    except Exception as e:
        logging.error(f"Ошибка при обработке /start: {e}")
        logging.error(traceback.format_exc())

# Обработчик команды /stop и кнопки "⛔ Стоп"
@router.message(lambda message: message.text == "⛔ Стоп" or message.text == "/stop")
async def stop_game(message: types.Message, state: FSMContext):
    try:
        logging.info("Game stopped")
        user_id = str(message.from_user.id)
        points = stats.get(user_id, {}).get("points", 0)
        await state.update_data(in_game=False)
        stats[user_id]["in_game"] = False
        save_stats(stats)
        await message.answer(f"Игра остановлена. Ты набрал {points} очков. Нажми кнопку ниже, чтобы начать заново.", reply_markup=start_keyboard)
    except Exception as e:
        logging.error(f"Ошибка при обработке /stop: {e}")
        logging.error(traceback.format_exc())

# Обработчик команды /stat и кнопки "📊 Статистика"
@router.message(lambda message: message.text == "📊 Статистика" or message.text == "/stat")
async def show_stats(message: types.Message, state: FSMContext):
    try:
        user_id = str(message.from_user.id)
        points = stats.get(user_id, {}).get("points", 0)
        await message.answer(f"📊 Твоя статистика: {points} очков")
    except Exception as e:
        logging.error(f"Ошибка при обработке статистики: {e}")
        logging.error(traceback.format_exc())

# Обработчик кнопки "🚀 Начать игру"
@router.message(lambda message: message.text == "🚀 Начать игру")
async def restart_game(message: types.Message, state: FSMContext):
    try:
        logging.info("Game restarted")
        user_id = str(message.from_user.id)
        stats[user_id]["in_game"] = True
        save_stats(stats)
        await state.update_data(in_game=True)
        await message.answer("Игра началась! Выбирай:", reply_markup=game_keyboard)
    except Exception as e:
        logging.error(f"Ошибка при перезапуске игры: {e}")
        logging.error(traceback.format_exc())

# Обработчики кнопок "Правда" и "Действие"
@router.message(lambda message: message.text == "🎭 Правда")
async def truth_handler(message: types.Message, state: FSMContext):
    try:
        logging.info("Truth selected")
        user_id = str(message.from_user.id)
        if stats.get(user_id, {}).get("in_game", False):
            stats[user_id]["points"] += 1
            save_stats(stats)
            await message.answer(f"{random.choice(truths)}\n\nТы получил 1 очко! Всего очков: {stats[user_id]['points']}")
        else:
            await message.answer("Для начала игры нажми '🚀 Начать игру'.")
    except Exception as e:
        logging.error(f"Ошибка при выборе 'Правда': {e}")
        logging.error(traceback.format_exc())

@router.message(lambda message: message.text == "💪 Действие")
async def dare_handler(message: types.Message, state: FSMContext):
    try:
        logging.info("Dare selected")
        user_id = str(message.from_user.id)
        if stats.get(user_id, {}).get("in_game", False):
            stats[user_id]["points"] += 1
            save_stats(stats)
            await message.answer(f"{random.choice(dares)}\n\nТы получил 1 очко! Всего очков: {stats[user_id]['points']}")
        else:
            await message.answer("Для начала игры нажми '🚀 Начать игру'.")
    except Exception as e:
        logging.error(f"Ошибка при выборе 'Действие': {e}")
        logging.error(traceback.format_exc())

# Запуск бота
async def main():
    try:
        await set_commands(bot)
        logging.info("Starting bot...")
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
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
