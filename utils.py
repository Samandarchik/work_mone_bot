# utils.py
"""
Yordamchi funksiyalar
"""

from datetime import datetime, date
import config

def format_date(target_date):
    """Sanani o'zbekcha formatda chiqarish"""
    day = target_date.day
    month = config.MONTHS[target_date.month]
    year = target_date.year
    weekday = config.WEEKDAYS[target_date.weekday()]
    
    return f"{day}-{month}, {year}-yil ({weekday})"


def format_phone(phone):
    """Telefon raqamini formatda ko'rsatish"""
    phone_str = str(phone)
    return f"+{phone_str}"


def get_status_emoji(percentage):
    """Foiz bo'yicha emoji berish"""
    if percentage >= 80:
        return config.STATUS_EMOJI[100]
    elif percentage >= 50:
        return config.STATUS_EMOJI[80]
    elif percentage >= 1:
        return config.STATUS_EMOJI[50]
    else:
        return config.STATUS_EMOJI[0]

def format_user_tasks_message(user_data, tasks, target_date):
    """User uchun vazifalar ro'yxati xabarini yaratish"""
    
    # User ma'lumotlari
    user_id, telegram_id, full_name, phone, filial_id, filial_name, role_id, role_name, is_admin = user_data
    
    # Vazifalarni guruhlash
    daily_tasks = []
    monday_tasks = []
    monthly_tasks = []
    total_incomplete = 0
    
    for task_id, task_text, task_type, completed in tasks:
        if not completed:
            total_incomplete += 1
        
        if task_type == 'daily':
            daily_tasks.append((task_id, task_text, completed))
        elif task_type == 'monday':
            monday_tasks.append((task_id, task_text, completed))
        elif task_type == 'monthly':
            monthly_tasks.append((task_id, task_text, completed))
    
    # Xabar matni
    message = f"""<b>📋 SIZNING VAZIFALARINGIZ\n\n</b>"""
    
    if total_incomplete > 0:
        message += f"Bajarilmagan vazifalar: {total_incomplete} ta"
    else:
        message += "✅ Barcha vazifalar bajarildi!"
    
    return message


def format_task_completion_caption(user_data, task_text):
    """Vazifa bajarilganligi haqida guruhga yuborish uchun caption"""
    user_id, telegram_id, full_name, phone, filial_id, filial_name, role_id, role_name, is_admin = user_data
    
    
    
    caption = f"""<b>📌 VAZIFA BAJARILDI</b>

👤 Ishchi: {full_name}
📱 Telefon: {format_phone(phone)}
📝 Vazifa: {task_text}"""
    
    return caption


def format_filial_statistics(stats, date_obj):
    """
    Filiallar statistikasi matnini yaratish
    """
    date_str = date_obj.strftime("%Y-%m-%d")
    msg = f"📊 <b>{date_str} — Filiallar bo‘yicha kunlik statistika</b>\n\n"

    for filial_id, filial_name, total, completed in stats:
        
        percent = 0
        if total > 0:
            percent = round((completed / total) * 100, 1)

        msg += (
            f"🏢 <b>{filial_name}</b>\n"
            f"— Jami vazifalar: <b>{total} ta</b>\n"
            f"— Bajarilgan: <b>{completed} ta</b>\n"
            f"— Natija: <b>{percent}%</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
        )
    
    return msg
