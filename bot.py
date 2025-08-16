from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# جایگزین کن با توکن ربات خودت
TOKEN = "7644788893:AAHXHJf-6I4lDs6WgIEtR0SMTNUtJtyVg6U"

# مرحله‌های گفتگو
GRADE, FIELD, SUBJECT, MESSAGE = range(4)

# شروع ربات
def start(update, context):
    update.message.reply_text(
        "سلام! 👋\nبرای ارسال پیام ناشناس پایه‌ت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup([["دهم", "یازدهم", "دوازدهم"]], one_time_keyboard=True)
    )
    return GRADE

# دریافت پایه
def grade(update, context):
    context.user_data["grade"] = update.message.text
    update.message.reply_text(
        "رشته‌ت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup([["تجربی", "ریاضی", "انسانی"]], one_time_keyboard=True)
    )
    return FIELD

# دریافت رشته
def field(update, context):
    context.user_data["field"] = update.message.text
    update.message.reply_text("موضوع پیام رو بنویس (مثال: مشکل با اولیا):")
    return SUBJECT

# دریافت موضوع
def subject(update, context):
    context.user_data["subject"] = update.message.text
    update.message.reply_text("حالا متن کامل پیام‌ت رو بنویس:")
    return MESSAGE

# دریافت متن اصلی و ارسال به ادمین
def message(update, context):
    user_message = update.message.text
    grade = context.user_data["grade"]
    field = context.user_data["field"]
    subject = context.user_data["subject"]

    final_text = f"#{grade} #{field} #{subject}\n{user_message}"

    # آیدی عددی ادمین (باید جایگزین کنی)
    ADMIN_ID = 123456789
    context.bot.send_message(chat_id=ADMIN_ID, text=final_text)

    update.message.reply_text("پیام‌ت ناشناس ارسال شد ✅")
    return ConversationHandler.END

# لغو عملیات
def cancel(update, context):
    update.message.reply_text("عملیات لغو شد ❌")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GRADE: [MessageHandler(Filters.text & ~Filters.command, grade)],
            FIELD: [MessageHandler(Filters.text & ~Filters.command, field)],
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, subject)],
            MESSAGE: [MessageHandler(Filters.text & ~Filters.command, message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
