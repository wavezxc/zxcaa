import logging
from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ChatJoinRequestHandler, ContextTypes
)

BOT_TOKEN = "7620394182:AAECtDKzVycDeJGsiJgJOew7DT6hzCeDAis"
PUBLIC_CHANNEL = "@SHOW_RAID"
PRIVATE_LINKS = [
    "https://t.me/+foi7I0BJaVg1MWEy",
    "https://t.me/+jDom-KGLSHlkNWQy"
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id=PUBLIC_CHANNEL, user_id=user.id)
        status = member.status
    except Exception as e:
        logging.error(f"Ошибка при get_chat_member: {e}")
        status = None

    if status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        text = "✅ Вы подписаны на канал @SHOW_RAID. Заявки в приватные каналы будут одобрены автоматически.\n\n"
        text += "\n".join(f"- {link}" for link in PRIVATE_LINKS)
    else:
        text = "❌ Подпишитесь на канал @SHOW_RAID и напишите /start ещё раз."

    await context.bot.send_message(chat_id=chat_id, text=text)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user_id = request.from_user.id
    chat_id = request.chat.id
    try:
        member = await context.bot.get_chat_member(chat_id=PUBLIC_CHANNEL, user_id=user_id)
        status = member.status
    except Exception as e:
        logging.error(f"Ошибка при get_chat_member: {e}")
        status = None

    if status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
        logging.info(f"✅ Заявка одобрена: {user_id}")
    else:
        await context.bot.decline_chat_join_request(chat_id=chat_id, user_id=user_id)
        logging.info(f"❌ Заявка отклонена: {user_id}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.run_polling()
