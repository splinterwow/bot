# Video Xabarni Sozlash

## WELCOME_VIDEO_ID ni olish

Start bosilganda ko'rsatiladigan video xabarni sozlash uchun quyidagi qadamlarni bajaring:

### 1-qadam: Video xabar tayyorlash

Telegram'da dumaloq video (video note) yoki oddiy video tayyorlang. Bu video start bosilganda foydalanuvchilarga ko'rsatiladi.

### 2-qadam: Video ID ni olish

1. Botingizni ishga tushiring: `python bot.py`
2. Telegram'da botingizga shaxsiy xabar yozing
3. **Dumaloq video** (video note) yoki oddiy video yuboring
4. Bot sizga file_id ni ko'rsatadi:

\`\`\`
✅ Video Note (Dumaloq video) qabul qilindi!

📹 File ID:
DQACAgIAAxkBAAIC...

Bu ID ni .env fayliga qo'shing:
WELCOME_VIDEO_ID=DQACAgIAAxkBAAIC...

Keyin botni qayta ishga tushiring.
\`\`\`

### 3-qadam: .env fayliga qo'shish

File ID ni nusxalab oling va `.env` faylingizga qo'shing:

\`\`\`env
TELEGRAM_BOT_TOKEN=sizning_bot_tokeningiz
ADMIN_CHAT_ID=-1001234567890
MEDIA_CHANNEL_ID=-1009876543210
WELCOME_VIDEO_ID=DQACAgIAAxkBAAIC...
\`\`\`

### 4-qadam: Botni qayta ishga tushirish

Botni to'xtatib (Ctrl+C) qayta ishga tushiring:

\`\`\`bash
python bot.py
\`\`\`

Endi /start bosilganda avval video xabar, keyin lavozim tanlash tugmalari ko'rsatiladi!

## Muhim eslatmalar

- **Dumaloq video** (video note) ishlatish tavsiya etiladi - rasmda ko'rsatilgandek
- Agar dumaloq video ishlamasa, oddiy video ham ishlaydi
- Video file_id faqat bir marta olish kerak
- Har safar yangi video qo'ymoqchi bo'lsangiz, yuqoridagi jarayonni takrorlang

## Muammolarni hal qilish

**Video ko'rsatilmayapti:**
- `.env` faylda `WELCOME_VIDEO_ID` to'g'ri yozilganligini tekshiring
- Botni qayta ishga tushirganingizni tekshiring
- File ID to'g'ri nusxalanganligini tekshiring (bo'sh joy yoki qo'shimcha belgilar bo'lmasligi kerak)

**"Video not found" xatosi:**
- Video file_id eskirgan bo'lishi mumkin
- Yangi video yuborib, yangi file_id oling
