# scheduler.py
"""
Avtomatik xabarlar - kunlik statistika
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta, date
from aiogram import Bot

from database import db
from utils import format_filial_statistics
import config

scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)

async def send_filial_statistics(bot: Bot):
    """Har bir filial bo‘yicha kunlik umumiy statistika yuborish"""
    
    yesterday = date.today() - timedelta(days=1)

    stats = db.get_filial_task_statistics(yesterday)
    msg = format_filial_statistics(stats, yesterday)

    await bot.send_message(
        chat_id=config.DAILY_STATS_GROUP_ID,
        text=msg,
    )


def setup_scheduler(bot: Bot):
    """Schedulerni sozlash"""
    
    # Har kuni soat 00:00 da
    scheduler.add_job(
        send_filial_statistics,
        trigger=CronTrigger(hour=13, minute=6),
        args=[bot],
        id='daily_statistics',
        name='Kunlik statistika yuborish',
        replace_existing=True
    )
    
    # Test uchun - har 10 daqiqada (ISHLATISHDAN OLDIN O'CHIRIB QO'YISH KERAK!)
    # scheduler.add_job(
    #     send_daily_statistics,
    #     trigger=CronTrigger(minute='*/10'),
    #     args=[bot],
    #     id='test_statistics',
    #     name='Test statistika',
    #     replace_existing=True
    # )
    
    print("✅ Scheduler sozlandi:")
    print("   - Kunlik statistika: Har kuni 00:00")
    
    scheduler.start()
    print("✅ Scheduler ishga tushdi!")

async def stop_scheduler():
    """Schedulerni to'xtatish"""
    try:
        if scheduler.running:
            await scheduler.shutdown(wait=True)
            print("🛑 Scheduler to'xtatildi!")
    except Exception as e:
        print(f"❌ Scheduler to'xtatishda xatolik: {e}")
