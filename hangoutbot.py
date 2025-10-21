import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Хранилище для каждого чата
polls = {}

async def гулять(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Используй: /[w, g, gulyat, walk, go] [время]\nНапример: /g 17:00")
        return

    time = " ".join(context.args)
    chat_id = update.message.chat_id

    polls[chat_id] = {
        "time": time,
        "yes": set(),
        "no": set(),
        "message_id": None
    }

    keyboard = [
        [InlineKeyboardButton("✅ Я сігмо", callback_data="yes"),
         InlineKeyboardButton("❌ Я пєдік", callback_data="no")]
    ]

    msg = await update.message.reply_text(
        f"🕕 Ідєм гулять в {time}?\n\n✅ Сігмо: —\n❌ Пєдікі: —",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    polls[chat_id]["message_id"] = msg.message_id


async def кнопка(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user = query.from_user.full_name

    if chat_id not in polls:
        return

    data = polls[chat_id]
    if query.data == "yes":
        data["no"].discard(user)
        data["yes"].add(user)
    else:
        data["yes"].discard(user)
        data["no"].add(user)

    yes_list = "\n".join(data["yes"]) if data["yes"] else "—"
    no_list = "\n".join(data["no"]) if data["no"] else "—"

    text = f"🕕 Ідєм гулять в {data['time']}?\n\n✅ Сігмо:\n{yes_list}\n\n❌  Пєдікі:\n{no_list}"

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Я Сігмо", callback_data="yes"),
             InlineKeyboardButton("❌ Я Пєдік", callback_data="no")]
        ])
    )


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ НЕ УКАЗАН ТОКЕН БОТА! Добавь переменную окружения BOT_TOKEN.")
    
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler(["walk", "gulyat", "g", "w", "go"], гулять))
    app.add_handler(CallbackQueryHandler(кнопка))

    print("✅ Бот запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
