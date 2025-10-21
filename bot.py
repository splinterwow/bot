import logging
import os
import re
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, POSITIONS, PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD, ADMIN_CHAT_ID, MEDIA_CHANNEL_ID, WELCOME_VIDEO_ID, ADMIN_PASSWORD
from questions import QUESTIONS
from excel_generator import create_excel_file
import httpx

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_sessions = {}
admin_sessions = {}
USERS_DATA_FILE = 'users_data.json'

def load_users_data():
    """Foydalanuvchi ma'lumotlarini fayldan yuklash"""
    if os.path.exists(USERS_DATA_FILE):
        try:
            with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users_data(data):
    """Foydalanuvchi ma'lumotlarini faylga saqlash"""
    with open(USERS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_name(text):
    """
    Ism validatsiyasi - faqat harflar va bo'sh joylar
    """
    if not text or text.strip() == '':
        return False, "Ism bo'sh bo'lishi mumkin emas."
    
    if text.strip().isdigit():
        return False, "Ism faqat raqamlardan iborat bo'lishi mumkin emas. Iltimos, to'liq ismingizni kiriting."
    
    if not any(c.isalpha() for c in text):
        return False, "Ism kamida bitta harf bo'lishi kerak."
    
    return True, None

def validate_date(text):
    """
    Sana validatsiyasi - kk.oo.yyyy formatida
    """
    if not text or text.strip() == '':
        return False, "Sana bo'sh bo'lishi mumkin emas."
    
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, text.strip()):
        return False, "Noto'g'ri format! Iltimos, kk.oo.yyyy formatida kiriting (masalan: 15.03.1995)"
    
    try:
        parts = text.strip().split('.')
        day = int(parts[0])
        month = int(parts[1])
        year = int(parts[2])
        
        if day < 1 or day > 31:
            return False, "Kun 1 dan 31 gacha bo'lishi kerak."
        
        if month < 1 or month > 12:
            return False, "Oy 1 dan 12 gacha bo'lishi kerak."
        
        if year < 1900 or year > 2010:
            return False, "Yil 1900 dan 2010 gacha bo'lishi kerak."
        
        return True, None
    except:
        return False, "Noto'g'ri sana! Iltimos, to'g'ri sana kiriting."

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /getid komandasi - Chat ID ni ko'rsatish
    """
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title if update.effective_chat.title else "Shaxsiy chat"
    
    message = f"📋 Chat ma'lumotlari:\n\n"
    message += f"Chat ID: `{chat_id}`\n"
    message += f"Chat turi: {chat_type}\n"
    message += f"Chat nomi: {chat_title}\n\n"
    message += f"Bu ID ni .env fayliga qo'shing:\n"
    message += f"`ADMIN_CHAT_ID={chat_id}`\n"
    message += f"yoki\n"
    message += f"`MEDIA_CHANNEL_ID={chat_id}`"
    
    await update.message.reply_text(message, parse_mode='Markdown')
    logger.info(f"Chat ID so'raldi: {chat_id} ({chat_type} - {chat_title})")

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Video yoki video_note yuborilganda file_id ni ko'rsatish
    """
    file_id = None
    file_type = None
    
    if update.message.video_note:
        file_id = update.message.video_note.file_id
        file_type = "Video Note (Dumaloq video)"
    elif update.message.video:
        file_id = update.message.video.file_id
        file_type = "Video"
    
    if file_id:
        message = f"✅ {file_type} qabul qilindi!\n\n"
        message += f"📹 File ID:\n`{file_id}`\n\n"
        message += f"Bu ID ni .env fayliga qo'shing:\n"
        message += f"`WELCOME_VIDEO_ID={file_id}`\n\n"
        message += f"Keyin botni qayta ishga tushiring."
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"{file_type} file_id olindi: {file_id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start komandasi - Botni boshlash
    """
    user_id = update.effective_user.id
    
    logger.info(f"Start komandasi: User ID={user_id}, Chat ID={update.effective_chat.id}")
    
    user_sessions[user_id] = {
        'current_question': 0,
        'data': {},
        'position': None,
        'voice_messages': [],
        'video_messages': []
    }
    
    if WELCOME_VIDEO_ID:
        try:
            await context.bot.send_video_note(
                chat_id=update.effective_chat.id,
                video_note=WELCOME_VIDEO_ID
            )
        except Exception as e:
            logger.error(f"Video note yuborishda xato: {e}")
            try:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=WELCOME_VIDEO_ID
                )
            except Exception as e2:
                logger.error(f"Video yuborishda ham xato: {e2}")
    
    keyboard = [
        [InlineKeyboardButton("Sotuv menejeri", callback_data='pos_sales')],
        [InlineKeyboardButton("SMM mutaxassisi", callback_data='pos_smm')],
        [InlineKeyboardButton("Kopirayter", callback_data='pos_copywriter')],
        [InlineKeyboardButton("Valantyor", callback_data='pos_volunteer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Kompaniyamizda qaysi lavozimda ishlamoqchisiz:",
        reply_markup=reply_markup
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /admin komandasi - Admin paneliga kirish
    """
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("Iltimos, parol bilan /admin parol buyrug'ini yuboring.")
        return
    
    password = ' '.join(context.args)
    
    if password != ADMIN_PASSWORD:
        await update.message.reply_text("Noto'g'ri parol!")
        logger.warning(f"Noto'g'ri admin paroli: User ID={user_id}")
        return
    
    admin_sessions[user_id] = True
    
    users_data = load_users_data()
    
    if not users_data:
        await update.message.reply_text("Hozircha ariza yo'q.")
        return
    
    context.user_data['admin_page'] = 0
    await show_admin_users_page(update, context, user_id, users_data, page=0)

async def show_admin_users_page(update: Update, context: ContextTypes.DEFAULT_TYPE, admin_id: int, users_data: dict, page: int = 0):
    """
    Admin paneliga foydalanuvchilarni sahifalar bo'yicha ko'rsatish
    """
    users_list = list(users_data.items())
    total_users = len(users_list)
    users_per_page = 10
    total_pages = (total_users + users_per_page - 1) // users_per_page
    
    if page < 0 or page >= total_pages:
        page = 0
    
    start_idx = page * users_per_page
    end_idx = start_idx + users_per_page
    page_users = users_list[start_idx:end_idx]
    
    keyboard = []
    for uid, user_info in page_users:
        button_text = f"{user_info.get('full_name', 'Noma\'lum')} - {user_info.get('position', 'Noma\'lum')}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"admin_user_{uid}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Orqaga", callback_data=f"admin_page_{page-1}"))
    
    page_info = f"Sahifa {page + 1}/{total_pages}"
    nav_buttons.append(InlineKeyboardButton(page_info, callback_data="admin_page_info"))
    
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Oldinga ➡️", callback_data=f"admin_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"Ariza bergan odamlar ro'yxati ({total_users} ta):\n\nKimga xabar yubormoqchisiz?"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message_text, reply_markup=reply_markup)

async def admin_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin foydalanuvchini tanladi - batafsil ma'lumot ko'rsatish
    """
    query = update.callback_query
    await query.answer()
    
    admin_id = update.effective_user.id
    
    if admin_id not in admin_sessions:
        await query.edit_message_text("Iltimos, avval /admin parol bilan kiriting.")
        return
    
    user_id = query.data.replace('admin_user_', '')
    
    context.user_data['selected_user_id'] = user_id
    
    users_data = load_users_data()
    user_info = users_data.get(user_id, {})
    
    timestamp = user_info.get('timestamp', 'Noma\'lum')
    
    message = f"📋 Tanlangan foydalanuvchi:\n\n"
    message += f"👤 Ism: {user_info.get('full_name', 'Noma\'lum')}\n"
    message += f"💼 Lavozim: {user_info.get('position', 'Noma\'lum')}\n"
    message += f"📱 Telefon: {user_info.get('phone', 'Noma\'lum')}\n"
    message += f"🆔 User ID: {user_id}\n"
    message += f"📅 Ariza sanasi: {timestamp}\n\n"
    message += f"💬 Xabar yozing:"
    
    await query.edit_message_text(message)

async def admin_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin panel sahifalarini o'tish
    """
    query = update.callback_query
    await query.answer()
    
    admin_id = update.effective_user.id
    
    if admin_id not in admin_sessions:
        await query.edit_message_text("Iltimos, avval /admin parol bilan kiriting.")
        return
    
    page = int(query.data.replace('admin_page_', ''))
    
    users_data = load_users_data()
    await show_admin_users_page(query, context, admin_id, users_data, page=page)

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin foydalanuvchiga xabar yuboradi
    """
    admin_id = update.effective_user.id
    
    if admin_id not in admin_sessions or 'selected_user_id' not in context.user_data:
        return
    
    user_id = int(context.user_data['selected_user_id'])
    message_text = update.message.text
    
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📬 Kompaniyadan sizga xabar:\n\n{message_text}"
        )
        
        await update.message.reply_text("Xabar yuborildi!")
        logger.info(f"Admin xabar yubordi: Admin ID={admin_id}, User ID={user_id}")
        
        del context.user_data['selected_user_id']
        del admin_sessions[admin_id]
    except Exception as e:
        await update.message.reply_text(f"Xabar yuborishda xato: {e}")
        logger.error(f"Admin xabar yuborishda xato: {e}")

async def position_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Lavozim tanlanganda
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    position_key = query.data.replace('pos_', '')
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'current_question': 0,
            'data': {},
            'position': None,
            'voice_messages': [],
            'video_messages': []
        }
    
    user_sessions[user_id]['position'] = POSITIONS[position_key]
    user_sessions[user_id]['data']['position'] = POSITIONS[position_key]
    
    await query.edit_message_text(
        f"Tanlangan lavozim: {POSITIONS[position_key]}\n\nEndi sizga bir nechta savol beramiz."
    )
    
    await ask_question(update, context, user_id)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """
    Keyingi savolni berish
    """
    session = user_sessions[user_id]
    question_index = session['current_question']
    
    if question_index >= len(QUESTIONS):
        await finish_survey(update, context, user_id)
        return
    
    question = QUESTIONS[question_index]
    
    progress = f"{question_index + 1}/{len(QUESTIONS)}"
    question_text = f"{progress}. {question['question']}"
    
    if question['type'] == 'text':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text,
            reply_markup=ReplyKeyboardRemove()
        )
    
    elif question['type'] == 'contact':
        keyboard = [[KeyboardButton(question['button_text'], request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text,
            reply_markup=reply_markup
        )
    
    elif question['type'] == 'buttons':
        keyboard = []
        for row in question['options']:
            keyboard.append([InlineKeyboardButton(btn, callback_data=f"ans_{question['id']}_{btn}") for btn in row])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text,
            reply_markup=reply_markup
        )
    
    elif question['type'] == 'voice':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text + "\n\n🎤 Ovozli xabar yuboring:",
            reply_markup=ReplyKeyboardRemove()
        )
    
    elif question['type'] == 'video':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text + "\n\n🎥 Video xabar yuboring:",
            reply_markup=ReplyKeyboardRemove()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Foydalanuvchi xabarlarini qayta ishlash
    """
    user_id = update.effective_user.id
    
    if user_id in admin_sessions and 'selected_user_id' in context.user_data:
        await handle_admin_message(update, context)
        return
    
    if user_id not in user_sessions or user_sessions[user_id]['position'] is None:
        if update.message.video or update.message.video_note:
            await get_video_id(update, context)
            return
        
        if user_id in user_sessions and user_sessions[user_id]['position'] is None:
            await update.message.reply_text("Iltimos, avval lavozimni tanlang.")
            return
        
        await update.message.reply_text("Iltimos, /start buyrug'ini bosing.")
        return
    
    session = user_sessions[user_id]
    question_index = session['current_question']
    
    if question_index >= len(QUESTIONS):
        return
    
    question = QUESTIONS[question_index]
    
    if question['type'] == 'text' and not update.message.text:
        await update.message.reply_text("Iltimos, matn javob yuboring.")
        return
    
    if question['type'] == 'text':
        text_answer = update.message.text
        
        if 'validation' in question:
            if question['validation'] == 'name':
                is_valid, error_msg = validate_name(text_answer)
                if not is_valid:
                    await update.message.reply_text(f"❌ {error_msg}")
                    return
            elif question['validation'] == 'date':
                is_valid, error_msg = validate_date(text_answer)
                if not is_valid:
                    await update.message.reply_text(f"❌ {error_msg}")
                    return
        
        session['data'][question['key']] = text_answer
        session['current_question'] += 1
        await ask_question(update, context, user_id)
    
    elif question['type'] == 'contact':
        if update.message.contact:
            session['data'][question['key']] = update.message.contact.phone_number
            session['current_question'] += 1
            await ask_question(update, context, user_id)
        else:
            await update.message.reply_text("Iltimos, telefon raqamingizni yuboring.")
    
    elif question['type'] == 'voice':
        if update.message.voice:
            session['voice_messages'].append({
                'file_id': update.message.voice.file_id,
                'question_id': question['id'],
                'question_label': question['label']
            })
            session['data'][question['key']] = f"🎤 Ovozli xabar #{question['id']}"
            session['current_question'] += 1
            await ask_question(update, context, user_id)
        else:
            await update.message.reply_text("Iltimos, ovozli xabar yuboring.")
    
    elif question['type'] == 'video':
        if update.message.video or update.message.video_note:
            video_file = update.message.video_note if update.message.video_note else update.message.video
            session['video_messages'].append({
                'file_id': video_file.file_id,
                'question_id': question['id'],
                'question_label': question['label']
            })
            session['data'][question['key']] = f"🎥 Video xabar #{question['id']}"
            session['current_question'] += 1
            await ask_question(update, context, user_id)
        else:
            await update.message.reply_text("Iltimos, video xabar yuboring.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Inline tugma bosilganda
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await query.edit_message_text("Iltimos, /start buyrug'ini bosing.")
        return
    
    if query.data.startswith('ans_'):
        parts = query.data.split('_', 2)
        question_id = int(parts[1])
        answer = parts[2]
        
        session = user_sessions[user_id]
        question = QUESTIONS[session['current_question']]
        
        session['data'][question['key']] = answer
        
        await query.edit_message_text(
            f"{question['question']}\n\n✅ Javob: {answer}"
        )
        
        session['current_question'] += 1
        await ask_question(update, context, user_id)
    
    elif query.data.startswith('admin_user_'):
        await admin_user_callback(update, context)

async def finish_survey(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """
    So'rovnoma tugagach - barcha media va Excel ni bir vaqtda yuborish
    """
    session = user_sessions[user_id]
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ Ma'lumotlaringiz qabul qilindi. Tez orada xabar beramiz!",
        reply_markup=ReplyKeyboardRemove()
    )
    
    logger.info(f"Yangi ariza qabul qilindi:")
    logger.info(f"Lavozim: {session['data'].get('position', 'Noma\'lum')}")
    logger.info(f"Ism: {session['data'].get('full_name', 'Noma\'lum')}")
    
    timestamp_str = datetime.now().strftime('%d.%m.%Y')
    
    users_data = load_users_data()
    users_data[str(user_id)] = {
        'user_id': user_id,
        'position': session['data'].get('position', 'Noma\'lum'),
        'full_name': session['data'].get('full_name', 'Noma\'lum'),
        'phone': session['data'].get('phone', 'Noma\'lum'),
        'timestamp': timestamp_str
    }
    save_users_data(users_data)
    
    voice_links = []
    for voice_msg in session['voice_messages']:
        try:
            sent_msg = await context.bot.send_voice(
                chat_id=MEDIA_CHANNEL_ID,
                voice=voice_msg['file_id'],
                caption=f"🎤 {session['data'].get('full_name', 'Noma\'lum')} - {voice_msg['question_label']}"
            )
            channel_id = str(MEDIA_CHANNEL_ID).replace('-100', '')
            voice_link = f"https://t.me/c/{channel_id}/{sent_msg.message_id}"
            voice_links.append({
                'question_label': voice_msg['question_label'],
                'link': voice_link
            })
            logger.info(f"Ovozli xabar yuborildi: {voice_msg['question_label']}")
        except Exception as e:
            logger.error(f"Ovozli xabar yuborishda xato: {e}")
    
    video_links = []
    for video_msg in session['video_messages']:
        try:
            sent_msg = await context.bot.send_video(
                chat_id=MEDIA_CHANNEL_ID,
                video=video_msg['file_id'],
                caption=f"🎥 {session['data'].get('full_name', 'Noma\'lum')} - {video_msg['question_label']}"
            )
            channel_id = str(MEDIA_CHANNEL_ID).replace('-100', '')
            video_link = f"https://t.me/c/{channel_id}/{sent_msg.message_id}"
            video_links.append({
                'question_label': video_msg['question_label'],
                'link': video_link
            })
            logger.info(f"Video xabar yuborildi: {video_msg['question_label']}")
        except Exception as e:
            logger.error(f"Video xabar yuborishda xato: {e}")
    
    for voice_link in voice_links:
        for question in QUESTIONS:
            if question['label'] == voice_link['question_label']:
                session['data'][question['key']] = voice_link['link']
    
    for video_link in video_links:
        for question in QUESTIONS:
            if question['label'] == video_link['question_label']:
                session['data'][question['key']] = video_link['link']
    
    try:
        excel_path = create_excel_file(session['data'])
        with open(excel_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=ADMIN_CHAT_ID,
                document=file,
                caption=f"📋 Yangi ariza\n\nLavozim: {session['data'].get('position', 'Noma\'lum')}\nIsm: {session['data'].get('full_name', 'Noma\'lum')}\nTelefon: {session['data'].get('phone', 'Noma\'lum')}"
            )
        os.remove(excel_path)
        logger.info(f"Excel fayl admin kanalga yuborildi")
    except Exception as e:
        logger.error(f"Excel yuborishda xato: {e}")
    
    del user_sessions[user_id]

def main():
    """
    Botni ishga tushirish
    """
    builder = Application.builder().token(BOT_TOKEN)
    
    if PROXY_URL:
        logger.info(f"Proxy ishlatilmoqda: {PROXY_URL}")
        
        proxy_auth = None
        if PROXY_USERNAME and PROXY_PASSWORD:
            proxy_auth = httpx.BasicAuth(PROXY_USERNAME, PROXY_PASSWORD)
        
        httpx_client = httpx.AsyncClient(
            proxy=PROXY_URL,
            auth=proxy_auth,
            timeout=30.0
        )
        
        from telegram.request import HTTPXRequest
        request = HTTPXRequest(http_version="1.1", client=httpx_client)
        builder = builder.request(request)
    
    application = builder.build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getid", get_id))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(position_callback, pattern='^pos_'))
    application.add_handler(CallbackQueryHandler(admin_page_callback, pattern='^admin_page_'))
    application.add_handler(CallbackQueryHandler(button_callback, pattern='^ans_|^admin_user_'))
    application.add_handler(MessageHandler(filters.TEXT | filters.CONTACT | filters.VOICE | filters.VIDEO | filters.VIDEO_NOTE, handle_message))
    
    logger.info("Bot ishga tushdi...")
    logger.info("Kanal ID ni olish uchun kanalga /getid buyrug'ini yuboring")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
