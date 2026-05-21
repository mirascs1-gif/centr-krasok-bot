"""
Telegram AI-бот для «Центр Красок #1»
======================================
Запуск:
    pip install python-telegram-bot google-generativeai
    python bot.py
"""

import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Вставьте свои токены ─────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8808605575:AAHqbozqgBNqAz5hkeGm9vcguuTdXgz9c0Y")
GEMINI_KEY     = os.getenv("GEMINI_KEY",     "AIzaSyBtYYdHC3pWAxz0L9Rspz-PXADfe9MKiiM")

# ─── База знаний ──────────────────────────────────────────────────────────────
COMPANY_KNOWLEDGE = """
=== БАЗА ЗНАНИЙ: «Центр Красок #1» ===

## О компании
«Центр Красок #1» — интернет-магазин строительных красок, лаков, штукатурок и малярных
инструментов премиум- и ультра-премиум-класса в Казахстане. Официальный дистрибьютор
ведущих европейских брендов. Юридическое лицо: ТОО «SAMRUk Trade», БИН 140640024284.

## Контакты и адреса

### Алматы — магазин 1 (шоу-рум)
Адрес: г. Алматы, ул. Кабдолова 1/8, блок 1, 1 ряд, линия D, бутик 14
Телефоны: +7 778 061-50-00 / +7 701 877-50-00 / +7 701 974-50-00
Режим работы: пн–вс, 10:00–20:00

### Алматы — магазин 2
Адрес: г. Алматы, ул. Кабдолова 1/8, блок 1, 1 ряд, линия D, бутик 21
Телефон: +7 778 800-44-42 / +7 778 800-44-45
Режим работы: пн–вс, 10:00–20:00

### Астана
Адрес: г. Астана, ул. Мангилик Ел, 29/2
Телефон: +7 701 943-50-00
Режим работы: пн–вс, 10:00–20:00

Email: info@centr-krasok.kz
Сайт: https://centr-krasok.kz/

## Социальные сети
Instagram: https://www.instagram.com/centr_krasok/
Facebook: https://www.facebook.com/profile.php?id=100075230594445
YouTube: https://www.youtube.com/channel/UCPC7__jM5FzQXQOgqsNbUlQ

## Ассортимент
- Интерьерные краски (для гостиной, детской, кухни/ванной, потолков, стен)
- Фасадные краски
- Краски по дереву (мебель, окна/двери, пол/лестницы)
- Краски по металлу (молотковые, гладкие, полуматовые)
- Фактурные и декоративные краски / штукатурки
- Краски аэрозольные
- Лаки и масла (для полов, стен, древесины)
- Грунтовки (интерьерные, фасадные, универсальные)
- Антисептики и пропитки
- Шпатлевки и штукатурки
- Обои под покраску
- Клеи и герметики / монтажные пены
- Растворители и очистители
- Малярные инструменты (валики, кисти, шпатели, ленты, наждачная бумага и пр.)
- Краскопульты (ручные и электрические)
- Декоративная лепнина

## Бренды-партнёры (более 40)
Dulux, Hammerite, Pinotex, Marshall, Master Color, Oikos, Maitre Deco, Levis, Dufa,
KUDO, Anza, Profilux, Sikkens, PUFAS, MAKO, TEKNOS, Tytan, Profi Tec, STORCH,
Vetonit, Color Expert, Wagner, Argile, Orac Decor, Kelly-Moore, TimberCare, HYGGE,
PPL (Paint & Paper Library), Little Greene, Selena, KraftHaus, Quelyd, L'outil Parfait,
STRAIT-FLEX, TERRACO, DANOGIPS, Fiba Fuse, Charmant, Sikkens Heritage, Swiss Lake,
Masterline и другие. Страны: Италия, Франция, Великобритания, Нидерланды, США и др.

## Ключевые преимущества
- Более 45 000 оттенков колеровки
- 40+ брендов в ассортименте
- Сертифицированная и экологически чистая продукция
- Бесплатная консультация специалистов
- Доставка курьером или самовывоз из шоу-рума
- Акции, скидки и программа лояльности

## Для профессионалов
- Дизайнерам: скидки, бонусы, программа лояльности. Подробнее: centr-krasok.kz/designers/
- Строителям: centr-krasok.kz/for_builders/
- Корпоративным клиентам — особые условия

## Клиенты
МАСП, Casa Azzurra, Mossebo, Pinteriors, Alyer, One Space, Shafran, Шатура,
Umtyl edu, Rams City, Four Seasons, Центр Декора, Cappuccino, Desso, INTHAI,
Mega, Salvare, YA, mig и другие.

## Доставка и оплата
- Доставка: курьерская (до двери) или самовывоз из шоу-рума Алматы / Астана
- Оплата: Visa, Mastercard, Kaspi Pay
- Оформление заказа: через сайт centr-krasok.kz или по телефону
"""

SYSTEM_PROMPT = f"""Ты — дружелюбный и профессиональный AI-ассистент интернет-магазина «Центр Красок #1».

Правила:
1. Отвечай ТОЛЬКО на основе базы знаний ниже. Не придумывай факты.
2. Если информации нет в базе знаний — скажи об этом и предложи позвонить: +7 778 061-50-00 или написать на info@centr-krasok.kz.
3. Будь вежлив и лаконичен. Используй эмодзи умеренно (1–2 на сообщение).
4. На вопросы не по теме магазина — вежливо перенаправляй к теме.
5. На вопросы об адресах и контактах — давай точные данные из базы.

=== БАЗА ЗНАНИЙ ===
{COMPANY_KNOWLEDGE}
=== КОНЕЦ БАЗЫ ЗНАНИЙ ==="""

# ─── Инициализация Gemini ─────────────────────────────────────────────────────
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
)

# ─── История диалогов {user_id: chat_session} ────────────────────────────────
chat_sessions: dict = {}


def get_ai_response(user_id: int, user_message: str) -> str:
    try:
        if user_id not in chat_sessions:
            chat_sessions[user_id] = gemini_model.start_chat(history=[])
        response = chat_sessions[user_id].send_message(user_message)
        return response.text
    except Exception as e:
        logger.error("Ошибка Gemini API: %s", e)
        return "😔 Произошла техническая ошибка. Попробуйте позже или позвоните: +7 778 061-50-00"


# ─── Обработчики Telegram ─────────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text.strip()
    logger.info("Сообщение от %s (id=%s): %s", user.first_name, user.id, text)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = get_ai_response(user.id, text)
    await update.message.reply_text(reply)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_sessions.pop(user.id, None)
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я AI-ассистент магазина «Центр Красок #1» 🎨\n\n"
        "Задайте любой вопрос о нашем магазине:\n"
        "• Какие краски и бренды есть?\n"
        "• Где находятся магазины?\n"
        "• Как оформить заказ или доставку?\n"
        "• Условия для дизайнеров и строителей\n\n"
        "Просто напишите вопрос — я отвечу 💬"
    )


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_sessions.pop(update.effective_user.id, None)
    await update.message.reply_text("🔄 История очищена. Начнём заново!")


# ─── Точка входа ──────────────────────────────────────────────────────────────
def main() -> None:
    import asyncio
    from telegram.ext import CommandHandler

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("reset", handle_reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
