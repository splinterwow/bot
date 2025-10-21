# Telegram HR Bot

Bu bot ishga murojaat qiluvchilardan ma'lumot to'plash uchun mo'ljallangan.

## O'rnatish

### 1. Python o'rnatish
Python 3.8 yoki undan yuqori versiya kerak.

### 2. Loyihani yuklab oling
Barcha fayllarni bir papkaga yuklab oling.

### 3. Kutubxonalarni o'rnating
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Bot yaratish

1. Telegram'da @BotFather ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot uchun nom va username kiriting
4. BotFather sizga token beradi (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 5. Kanal va guruh yaratish

#### Admin kanali yaratish (Excel fayllar uchun):
1. Telegram'da yangi kanal yarating (masalan: "Olingan ma'lumotlar")
2. Kanalga botni admin qilib qo'shing
3. Kanal ID ni olish uchun:
   - @userinfobot ga o'ting
   - Kanaldan biror xabarni forward qiling
   - Bot sizga kanal ID ni beradi (masalan: `-1001234567890`)

#### Media kanali yaratish (ovoz/video uchun):
1. Yana bir kanal yarating (masalan: "Media fayllar")
2. Kanalga botni admin qilib qo'shing
3. Yuqoridagi usul bilan kanal ID ni oling

### 6. Environment variables sozlash

`.env.example` faylini `.env` ga nusxalang va quyidagilarni kiriting:

\`\`\`env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_CHAT_ID=-1001234567890
MEDIA_CHANNEL_ID=-1009876543210
\`\`\`

**Ixtiyoriy:** Boshlang'ich video qo'shish uchun:
1. Botga video yuboring
2. Logdan video file_id ni oling
3. `.env` ga qo'shing: `WELCOME_VIDEO_ID=BAACAgIAAxkBAAI...`

### 7. Botni ishga tushiring

\`\`\`bash
python bot.py
\`\`\`

Agar hammasi to'g'ri bo'lsa, `Bot ishga tushdi...` xabarini ko'rasiz.

## Botni sinab ko'rish

1. Telegram'da o'z botingizni toping
2. `/start` buyrug'ini yuboring
3. Lavozim tanlang
4. 23 ta savolga javob bering
5. Admin kanalingizda Excel fayl paydo bo'ladi
6. Media kanalingizda ovoz/video xabarlar paydo bo'ladi

## ⚠️ "Timed Out" xatosini hal qilish

Agar `telegram.error.TimedOut` xatosi chiqsa:

### Yechim 1: VPN ishlatish (Eng oson)
1. VPN dasturini yoqing
2. Botni qayta ishga tushiring

### Yechim 2: Proxy ishlatish
`.env` faylga proxy ma'lumotlarini qo'shing:

\`\`\`env
PROXY_URL=http://proxy_ip:proxy_port
PROXY_USERNAME=your_username
PROXY_PASSWORD=your_password
\`\`\`

## Hozirgi funksiyalar

Bot quyidagi funksiyalar bilan to'liq ishlaydi:

✅ /start komandasi
✅ 4 ta lavozim tanlash
✅ 23 ta savol berish (matn, tugma, ovoz, video)
✅ Javoblarni qabul qilish
✅ **Excel fayl yaratish va admin kanalga yuborish**
✅ **Video/ovoz fayllarni media kanalga forward qilish**
✅ Boshlang'ich video xabar (ixtiyoriy)

## Muammolarni hal qilish

### Bot ishlamayapti
1. Bot tokenni tekshiring
2. Internet aloqasini tekshiring
3. VPN/Proxy ishlatib ko'ring

### Excel fayl kelmayapti
1. `ADMIN_CHAT_ID` to'g'ri kiritilganligini tekshiring
2. Bot admin kanalda admin ekanligini tekshiring
3. Kanal ID `-100` bilan boshlanishi kerak

### Video/ovoz forward bo'lmayapti
1. `MEDIA_CHANNEL_ID` to'g'ri kiritilganligini tekshiring
2. Bot media kanalda admin ekanligini tekshiring

### Botni qanday to'xtatish kerak?
Terminal/CMD da `Ctrl+C` tugmalarini bosing

## Batafsil qo'llanma

`ISHLATISH_QOLLANMASI.md` faylida batafsil ko'rsatmalar mavjud.
