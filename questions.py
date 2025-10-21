# 19 ta yangi savol ro'yxati
QUESTIONS = [
    {
        'id': 1,
        'type': 'text',
        'question': 'Ism-familyangizni yozing:',
        'label': 'Ism-familiya',
        'key': 'full_name',
        'validation': 'name'
    },
    {
        'id': 2,
        'type': 'contact',
        'question': 'Telefon raqamingizni yuboring:',
        'label': 'Telefon raqam',
        'key': 'phone',
        'button_text': '📱 Telefon raqamni yuborish'
    },
    {
        'id': 3,
        'type': 'text',
        'question': 'Doimiy yashash manzilingizni yozing (propiska):',
        'label': 'Yashash manzili (propiska)',
        'key': 'address'
    },
    {
        'id': 4,
        'type': 'text',
        'question': 'Tug\'ilgan sanangizni yozing:\n\n📅 Format: kk.oo.yyyy (masalan: 05.05.2000)',
        'label': 'Tug\'ilgan sana',
        'key': 'birth_date',
        'validation': 'date'
    },
    {
        'id': 5,
        'type': 'buttons',
        'question': 'Ma\'lumotingiz:',
        'label': 'Ma\'lumot',
        'key': 'education',
        'options': [
            ['Oliy', 'O\'rta maxsus', 'Maktab o\'quvchisi']
        ]
    },
    {
        'id': 6,
        'type': 'text',
        'question': 'Oldin qayerda va qanday lavozimlarda ishlagansiz?',
        'label': 'Ish tajribasi',
        'key': 'work_experience'
    },
    {
        'id': 7,
        'type': 'buttons',
        'question': 'Oila qurganmisiz?',
        'label': 'Oilaviy ahvoli',
        'key': 'marital_status',
        'options': [
            ['Uylanganman', 'Turmush qurmaganman', 'Ajrashganman']
        ]
    },
    {
        'id': 8,
        'type': 'voice',
        'question': 'Golosovoy xabar yuboring (Oila a\'zolaringiz ota-onangiz, juftingiz va farzandlaringiz haqida ularni ismlari nima ish bilan mashg\'ulligi haqida):',
        'label': 'Oilaviy ahvoli',
        'key': 'voice_family'
    },
    {
        'id': 9,
        'type': 'video',
        'question': 'Dumaloq video qiling (O\'zingizni qiziqishlaringiz, kuchli va kuchsiz tomonlaringizni yozing):',
        'label': 'O\'zingiz haqingizda (video)',
        'key': 'video_intro'
    },
    {
        'id': 10,
        'type': 'buttons',
        'question': 'Oxirgi ish joyingizdan siz haqingizda surishtirishimizga rozimisiz?',
        'label': 'Rus tili darajasi',
        'key': 'reference_consent',
        'options': [
            ['Ha', 'Yo\'q']
        ]
    },
    {
        'id': 11,
        'type': 'text',
        'question': 'Oxirgi ish joyingizdan kim sizga tavsiya xati bera oladi, nomi, ishlash joyi, lavozimi, telefon raqami:\n\nMisol: Direktor - Malika Akramovna - Nona collection - +998909998877',
        'label': 'Tavsiya aloqasi',
        'key': 'reference_contact'
    },
    {
        'id': 12,
        'type': 'text',
        'question': 'Bizning korxonada qancha muddat ishlamoqchisiz?',
        'label': 'Qancha muddat ishlamoqchi',
        'key': 'work_duration'
    },
    {
        'id': 13,
        'type': 'text',
        'question': 'Korxonada ishdan keyin ham qolib ishlash kerak bo\'lib qolsa ishlaysizmi?',
        'label': 'Ortiqcha ishlash',
        'key': 'overtime'
    },
    {
        'id': 14,
        'type': 'text',
        'question': 'Sog\'ligingizda muammo yo\'qmi?',
        'label': 'Sog\'lik muammosi',
        'key': 'health_issues'
    },
    {
        'id': 15,
        'type': 'text',
        'question': 'Nima uchun ayrim odamlar ishga kech kelishadi?',
        'label': 'Kechikmaning sababi',
        'key': 'late_reasons'
    },
    {
        'id': 16,
        'type': 'text',
        'question': 'Nima uchun ayrim insonlar o\'g\'rilik qilishadi?',
        'label': 'O\'g\'rilik sababi',
        'key': 'theft_reasons'
    },
    {
        'id': 17,
        'type': 'text',
        'question': 'Nima uchun ayrim ishchilar yaxshi ishlashadi, ayrimlari yomon? Bunga sabab nima?',
        'label': 'Ish sifati sababi',
        'key': 'work_quality_reasons'
    },
    {
        'id': 18,
        'type': 'text',
        'question': 'Oldingi ishxonangizda qancha maoshga ishlagansiz?',
        'label': 'Oldingi maosh',
        'key': 'previous_salary'
    },
    {
        'id': 19,
        'type': 'text',
        'question': 'Bizning ishxonamizda qancha maoshga ishlamoqchisiz?',
        'label': 'Kerakli maosh',
        'key': 'desired_salary'
    }
]
