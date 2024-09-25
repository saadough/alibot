from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import os

# إعداد تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# دالة بدء البوت
def start(update, context):
    update.message.reply_text('مرحبًا! كيف يمكنني مساعدتك اليوم؟')

# دالة المساعدة
def help_command(update, context):
    update.message.reply_text('استخدم الأوامر التالية للتفاعل مع البوت:\n/start - لبدء المحادثة\n/help - للحصول على المساعدة\n/track - لتتبع الطلبات')

# دالة التعامل مع الرسائل
def handle_message(update, context):
    text = update.message.text
    update.message.reply_text(f'لقد قلت: {text}')

# دالة تتبع الطلبات
def track_order(update, context):
    tracking_id = context.args[0]
    api_key = os.getenv('7881482246:AAFzeyJtVgCJk1jINXGcKyoWBouuODsz7l8')
    response = requests.get(f'https://api.aliexpress.com/track/{tracking_id}', headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        update.message.reply_text(f'حالة الطلب: {response.json()["status"]}')
    else:
        update.message.reply_text('حدث خطأ أثناء تتبع الطلب. يرجى المحاولة مرة أخرى لاحقًا.')

def main():
    # إعداد البوت باستخدام توكن التلقرام
    updater = Updater(os.getenv('TELEGRAM_API_TOKEN'), use_context=True)
    dp = updater.dispatcher

    # إضافة الأوامر والمستمعين
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("track", track_order))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()