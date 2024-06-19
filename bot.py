from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, "Привет!")
        await send_text(update, context, f"Вы написали {update.message.text}")
        await send_photo(update, context, "main")
        await send_text_buttons(update, context, "Выберите режим работы:", {
            "btn_start": "Старт",
            "btn_stop": "Стоп"
        })


async def hello_buttons(update, context):
    query = update.callback_query.data  # код кнопки
    if query == "btn_start":
        await send_text(update, context, "Процесс запущен")
    else:
        await send_text(update, context, "Процесс остановлен")


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")

    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


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
    pass


async def date_buttons(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    await send_text(update, context, f"Кликнул по кнопке {query}", parse_mode.ParseMode.HTML)


dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="gpt:IMAtcJ134WVIxVeFe7I2JFkblB3TH88zgyZ5JYpVQKKxZnKk")
app = ApplicationBuilder().token("6891495771:AAETWhL-i06ruCp18eJLWKXeV0XEkRnnOLM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_buttons, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(hello_buttons))

app.run_polling()
