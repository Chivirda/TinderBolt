#!/usr/bin/python3

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    if dialog.mode == "message":
        await message_dialog(update, context)
    if dialog.mode == "profile":
        await profile_dialog(update, context)
    if dialog.mode == "opener":
        await opener_dialog(update, context)
    # else:
    #     await send_text(update, context, "Привет!")
    #     await send_text(update, context, f"Вы написали {update.message.text}")
    #     await send_photo(update, context, "main")
    #     await send_text_buttons(update, context, "Выберите режим работы:", {
    #         "btn_start": "Старт",
    #         "btn_stop": "Стоп"
    #     })


async def hello_buttons(update, context):
    query = update.callback_query.data  # код кнопки
    if query == "btn_start":
        await send_text(update, context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


async def gpt_dialog(update, context):
    my_message = await send_text(update, context, "ChatGPT думает. Ожидайте.")
    prompt = load_prompt("gpt")
    text = update.message.text
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)


async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })


async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослинг",
        "date_hardy": "Том Харди"
    })


async def date_dialog(update, context):
    my_message = await send_text(update, context, "Собеседник набирает текст. Ожидайте...")
    text = update.message.text
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_buttons(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Отличный выбор!")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, {
        "message_next": "Следующее сообщение",
        "message_date": "Пригласить на свидание"
    })
    dialog.list.clear()


async def message_buttons(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT думает над ответом...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def profile(update, context):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, context, "profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Сколько Вам лет?")


async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1
    if dialog.count == 1:
        dialog.user["age"] = text
        await send_text(update, context, "Кем Вы работаете?")
    elif dialog.count == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, "У Вас есть хобби?")
    elif dialog.count == 3:
        dialog.user["hobby"] = text
        await send_text(update, context, "Что Вам не нравится в людях?")
    elif dialog.count == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, "Цели знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("profile")
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "ChatGPT генерирует Ваш профиль...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


async def opener(update, context):
    dialog.mode = "opener"
    text = load_message("opener")
    await send_photo(update, context, "opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Имя девушки?")


async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "Сколько ей лет?")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "Оцените ее внешность: 1-10 баллов?")
    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, "Кем она работает?")
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "Цель знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "ChatGPT генерирует сообщение...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


dialog = Dialog()
dialog.mode = None
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService(token="gpt:IMAtcJ134WVIxVeFe7I2JFkblB3TH88zgyZ5JYpVQKKxZnKk")
app = ApplicationBuilder().token("6891495771:AAETWhL-i06ruCp18eJLWKXeV0XEkRnnOLM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_buttons, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_buttons, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_buttons))

app.run_polling()
