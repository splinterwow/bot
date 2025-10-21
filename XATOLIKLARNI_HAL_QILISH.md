# Xatoliklarni hal qilish

## 1. telegram.error.TimedOut: Timed out

**Sabab:** Telegram API serverlariga ulanib bo'lmayapti. Bu ko'pincha Telegram bloklangan mamlakatlarda yuz beradi.

**Yechimlar:**

### A) VPN ishlatish (Tavsiya etiladi)

1. **VPN dasturini o'rnating:**
   - Windows: ProtonVPN, Windscribe, TunnelBear
   - Bepul versiyalar mavjud

2. **VPN ni yoqing va botni qayta ishga tushiring:**
   \`\`\`bash
   python bot.py
   \`\`\`

### B) Proxy ishlatish

1. **Bepul proxy topish:**
   - https://www.proxy-list.download/
   - https://free-proxy-list.net/
   - HTTPS yoki SOCKS5 proxy tanlang

2. **`.env` faylga proxy qo'shing:**
   \`\`\`env
   PROXY_URL=http://123.456.789.012:8080
   \`\`\`

3. **Agar proxy parol talab qilsa:**
   \`\`\`env
   PROXY_URL=http://123.456.789.012:8080
   PROXY_USERNAME=username
   PROXY_PASSWORD=password
   \`\`\`

4. **Botni qayta ishga tushiring:**
   \`\`\`bash
   python bot.py
   \`\`\`

**Eslatma:** Bepul proxylar tez-tez ishlamay qolishi mumkin. Agar bitta proxy ishlamasa, boshqasini sinab ko'ring.

---

## 2. ModuleNotFoundError: No module named 'telegram'

**Sabab:** python-telegram-bot kutubxonasi o'rnatilmagan.

**Yechim:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

---

## 3. FileNotFoundError: [Errno 2] No such file or directory: '.env'

**Sabab:** `.env` fayli yo'q.

**Yechim:**
1. `.env.example` faylini `.env` ga nusxalang
2. Kerakli ma'lumotlarni kiriting

---

## 4. Excel fayl admin chatga kelmayapti

**Sabab:** ADMIN_CHAT_ID noto'g'ri yoki bot chatga xabar yubora olmayapti.

**Yechim:**
1. @userinfobot dan o'z chat ID ni oling
2. Botga `/start` yuboring (bot sizga xabar yubora olishi uchun)
3. `.env` faylda ADMIN_CHAT_ID ni tekshiring

---

## 5. Video/ovoz fayllar kanalga forward bo'lmayapti

**Sabab:** Bot kanalda admin emas yoki kanal ID noto'g'ri.

**Yechim:**
1. Botni kanalga admin qilib qo'shing
2. Kanal ID ni tekshiring (format: -100xxxxxxxxxx)
3. @userinfobot ni kanalga qo'shib, kanal ID ni oling

---

## 6. Bot sekin ishlayapti

**Sabab:** Bepul proxy sekin yoki internet aloqasi yomon.

**Yechim:**
1. Boshqa proxy sinab ko'ring
2. Pullik VPN xizmatidan foydalaning
3. Internet tezligini tekshiring

---

## 7. Bot to'xtab qoldi

**Sabab:** Xatolik yuz berdi yoki server o'chdi.

**Yechim:**
1. Terminal/CMD da xatolik xabarini o'qing
2. Botni qayta ishga tushiring:
   \`\`\`bash
   python bot.py
   \`\`\`
3. Agar muammo davom etsa, log fayllarni tekshiring

---

## Yordam kerakmi?

Agar yuqoridagi yechimlar yordam bermasa:
1. Terminal/CMD dagi to'liq xatolik xabarini nusxalang
2. `.env` faylni tekshiring (tokenlarni ko'rsatmang!)
3. Python versiyasini tekshiring: `python --version`
