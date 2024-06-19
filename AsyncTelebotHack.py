import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage
from telebot import types, asyncio_filters
import urllib.request
import os


bot = AsyncTeleBot('7159719757:AAEmKNi5T0wXDCkHG-8hxN115ZWCl7IQC6I', state_storage=StateMemoryStorage())

userFile = {}

userMode = {}

payload = {}

folderPath = ""

class Stages(StatesGroup):
    putfile = State()
    promt = State()

    customStage = State()
    customParams = State()

async def setAsyncStageFromUserMessage(message, stages, text: str):
    await bot.set_state(message.from_user.id, stages, message.chat.id)
    await bot.send_message(message.chat.id, text=text)

async def getAsyncData(message, key: str):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        result = data[key]
    return result

async def setAsyncData(message, key: str):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[key] = message.text

async def changeDataValue(message, key: str, elements):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[key] = elements

async def setUserMode(userId, mode):
    userMode[userId] = mode

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Базовый режим')
    itembtn2 = types.KeyboardButton('Продвинутый режим')
    markup.add(itembtn1, itembtn2)
    await bot.send_message(message.chat.id,
"Приветствую! Это бот для анализа и вывода актуальной метрики. Пожалуйста выберите режим обработки",
                        reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Очистка')
async def clear(message):
    userId = message.from_user.id
    if userId in userFile:
        os.remove(userFile[userId])
        del userFile[userId]
        await setAsyncStageFromUserMessage(message=message, stages=Stages.putfile,
                                           text="Файл удалён! Теперь вы можете установить новый файл.")
    else:
        await bot.send_message(message.chat.id, "У вас нету загруженный файлов")


@bot.message_handler(func=lambda message: message.text == 'Базовый режим')
async def basedMode(message):
    userId = message.from_user.id
    await setUserMode(message.from_user.id,"base")
    await bot.send_message(message.chat.id,"Установлен базовый режим работы.")
    if userId in userFile:
        await bot.send_message(message.chat.id, "Вы уже публиковали файл базы, чтобы удалить элемент введите 'Очистка'")
        return
    await setAsyncStageFromUserMessage(message=message, stages=Stages.putfile, text="Отправьте файл csv")

@bot.message_handler(func=lambda message: message.text == 'Продвинутый режим')
async def full_mode(message):
    await bot.send_message(message.chat.id, "Не реализован")

@bot.message_handler(state=Stages.putfile, content_types=['document'])
async def getFile(message):
    userId = message.from_user.id
    tr = None
    await bot.send_message(message.chat.id,"Выполняю загрузку файла...")
    if message.document:
        file_info = await bot.get_file(message.document.file_id)

        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

        tr = urllib.request.urlretrieve(photo_url, file_info.file_path)
    if tr:
        await bot.send_message(message.chat.id,"Файл сохранён как " + tr[0])
        userFile[userId] = tr[0]
    else:
        await bot.send_message(message.chat.id,"Не удалось сохранить файл")

@bot.message_handler(state=Stages.customStage)
async def chooseStage(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Вывод графиков')
    itembtn2 = types.KeyboardButton('Вывод числа')
    itembtn3 = types.KeyboardButton('Сопоставление параметров 1 и 2')
    markup.add(itembtn1, itembtn2, itembtn3)
    await bot.send_message(message.chat.id,
                           "Выберите тип обработки.",
                           reply_markup=markup)
    await setAsyncStageFromUserMessage(message=message, stages=Stages.customParams, text="")
    # TODO json format

@bot.message_handler(state=Stages.customParams)
async def chooseParams(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Доход')
    itembtn2 = types.KeyboardButton('Расход')
    itembtn3 = types.KeyboardButton('Чистая прибыль')
    markup.add(itembtn1, itembtn2, itembtn3)
    await bot.send_message(message.chat.id,
                           "Определите тип финансовой транзакции",
                           reply_markup=markup)







bot.add_custom_filter(asyncio_filters.StateFilter(bot))
asyncio.run(bot.polling())