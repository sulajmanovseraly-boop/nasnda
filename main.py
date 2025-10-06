import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8372633951:AAGNZQfYEfVw2qwIE0F3EB1y8hcuOxurBlw")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "1159623437"))

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище
messages = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["💡 Предложение", "⚠️ Жалоба"], ["🚀 Идея", "📚 Вопрос"]]
    await update.message.reply_text(
        "🎓 Анонимный Школьный Бот\n\n"
        "🔒 ВСЁ ПОЛНОСТЬЮ АНОНИМНО\n\n"
        "Выбери категорию:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # Определяем категорию
    category = "Сообщение"
    if "💡" in text: category = "Предложение"
    elif "⚠️" in text: category = "Жалоба" 
    elif "🚀" in text: category = "Идея"
    elif "📚" in text: category = "Вопрос"
    
    # Сохраняем
    msg_id = len(messages) + 1
    messages.append({
        'id': msg_id,
        'text': text.replace("💡", "").replace("⚠️", "").replace("🚀", "").replace("📚", "").strip(),
        'category': category,
        'user': f"@{user.username}" if user.username else f"ID:{user.id}",
        'name': user.first_name or ""
    })
    
    # Ответ пользователю
    await update.message.reply_text(f"✅ Отправлено анонимно! ID: #{msg_id}")
    
    # Уведомление админу
    await context.bot.send_message(
        ADMIN_CHAT_ID,
        f"🆕 #{msg_id} {category}\n"
        f"👤 {messages[-1]['name']} {messages[-1]['user']}\n"
        f"📝 {messages[-1]['text']}"
    )

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    
    if not messages:
        await update.message.reply_text("📭 Нет сообщений")
        return
    
    text = "📋 Сообщения:\n\n" + "\n".join(
        f"#{m['id']} {m['category']} - {m['user']}\n{m['text'][:50]}..." 
        for m in messages[-5:]
    )
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("view", view))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Бот запущен на Replit!")
    app.run_polling()

if __name__ == '__main__':
    main()
