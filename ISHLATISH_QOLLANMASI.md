# Bot bilan ishlash qo'llanmasi

## Botni birinchi marta ishga tushirish

### 1-qadam: Python o'rnatilganligini tekshirish

Terminal/CMD da quyidagi buyruqni yozing:

\`\`\`bash
python --version
\`\`\`

Agar Python 3.8 yoki undan yuqori versiya ko'rsatilsa, davom eting.

### 2-qadam: Loyihani yuklab olish

Barcha fayllarni bir papkaga yuklab oling.

### 3-qadam: Kutubxonalarni o'rnatish

Terminal/CMD da loyiha papkasiga o'ting va quyidagi buyruqni yozing:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4-qadam: Bot yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot uchun nom kiriting (masalan: "Mening HR Botim")
4. Bot uchun username kiriting (masalan: "mening_hr_bot")
5. BotFather sizga token beradi (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Bu tokenni nusxalab oling

### 5-qadam: .env fayl yaratish

1. `.env.example` faylini nusxalang va `.env` deb nomlang
2. `.env` faylni matn muharririda oching
3. `TELEGRAM_BOT_TOKEN=your_bot_token_here` qatorini toping
4. `your_bot_token_here` o'rniga o'zingizning tokeningizni qo'ying:

\`\`\`
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
\`\`\`

5. Faylni saqlang

### 6-qadam: Botni ishga tushirish

Terminal/CMD da quyidagi buyruqni yozing:

\`\`\`bash
python bot.py
\`\`\`

Agar hammasi to'g'ri bo'lsa, quyidagi xabarni ko'rasiz:

\`\`\`
Bot ishga tushdi...
\`\`\`

### 7-qadam: Botni sinab ko'rish

1. Telegram'da o'z botingizni toping (username orqali)
2. `/start` buyrug'ini yuboring
3. Bot sizga lavozimlarni taklif qiladi
4. Birini tanlang va savollarga javob bering

## Tez-tez beriladigan savollar

### Bot ishlamayapti, nima qilish kerak?

1. Bot token to'g'ri kiritilganligini tekshiring
2. Internet aloqangiz borligini tekshiring
3. Agar `TimedOut` xatosi bo'lsa, VPN yoqing yoki proxy ishlatib ko'ring

### Botni qanday to'xtatish kerak?

Terminal/CMD da `Ctrl+C` tugmalarini bosing.

### Botni qayta ishga tushirish kerak bo'lsa?

1. `Ctrl+C` bilan to'xtating
2. `python bot.py` buyrug'ini qayta yozing

### Ma'lumotlar qayerga saqlanadi?

Hozircha ma'lumotlar faqat bot xotirasida saqlanadi va konsolga chiqariladi. Keyinchalik Excel fayl va ma'lumotlar bazasi qo'shiladi.

## Keyingi qadamlar

Bot asosiy funksiyalar bilan ishlayapti. Keyinchalik qo'shiladi:

1. Excel fayl yaratish va yuborish
2. Ovoz/video fayllarni kanalga yuborish
3. Boshlang'ich video xabar
4. Ma'lumotlar bazasi

Hozircha bot barcha savollarni beradi va javoblarni qabul qiladi. Bu asosiy funksiyani sinab ko'rish uchun yetarli.
