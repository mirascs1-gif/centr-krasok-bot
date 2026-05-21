"""
Telegram AI-бот для «Центр Красок #1»
Запуск: pip install python-telegram-bot google-genai
"""

import os
import logging
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8808605575:AAFmbQPVPo3Ibeac1LMaRJQmRl5o7mKERhg")
GEMINI_KEY     = os.getenv("GEMINI_KEY",     "AIzaSyAu0_jnEZdL0NboPEP76TJHj8M6yuEVPA0")

COMPANY_KNOWLEDGE = """
=== БАЗА ЗНАНИЙ: «Центр Красок #1» ===

## О компании
«Центр Красок #1» — интернет-магазин строительных красок, лаков, штукатурок и малярных
инструментов премиум- и ультра-премиум-класса в Казахстане. Официальный дистрибьютор
ведущих европейских брендов. Юридическое лицо: ТОО «SAMRUk Trade», БИН 140640024284.

## Контакты и адреса

### Алматы — магазин 1
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
- Фактурные и декоративные краски, штукатурки
- Краски аэрозольные
- Лаки и масла (для полов, стен, древесины)
- Грунтовки (интерьерные, фасадные, универсальные)
- Антисептики и пропитки
- Шпатлевки и штукатурки
- Обои под покраску
- Клеи, герметики, монтажные пены
- Растворители и очистители
- Малярные инструменты (валики, кисти, шпатели, ленты, наждачная бумага)
- Краскопульты (ручные и электрические)
- Декоративная лепнина

## Бренды (более 40)
Dulux, Hammerite, Pinotex, Marshall, Master Color, Oikos, Maitre Deco, Levis, Dufa,
KUDO, Anza, Profilux, Sikkens, PUFAS, MAKO, TEKNOS, Tytan, Profi Tec, STORCH,
Vetonit, Color Expert, Wagner, Argile, Orac Decor, Kelly-Moore, TimberCare, HYGGE,
PPL, Little Greene, Selena, KraftHaus, Quelyd, STRAIT-FLEX, TERRACO, DANOGIPS,
Charmant, Sikkens Heritage, Swiss Lake, Masterline и другие.

## Преимущества
- Более 45 000 оттенков колеровки
- 40+ брендов в ассортименте
- Сертифицированная и экологически чистая продукция
- Бесплатная консультация специалистов
- Доставка курьером или самовывоз
- Акции, скидки и программа лояльности

## Для профессионалов
- Дизайнерам: скидки, бонусы, программа лояльности — centr-krasok.kz/designers/
- Строителям: centr-krasok.kz/for_builders/
- Корпоративным клиентам — особые условия

## Клиенты
МАСП, Casa Azzurra, Mossebo, Pinteriors, Alyer, One Space, Shafran, Шатура,
Umtyl edu, Rams City, Four Seasons, Центр Декора, Cappuccino, Desso, INTHAI,
Mega, Salvare, YA, mig и другие.

## Доставка и оплата
- Доставка: курьерская (до двери) или самовывоз из шоу-рума Алматы / Астана
- Оплата: Visa, Mastercard, Kaspi Pay
- Заказ: через сайт centr-krasok.kz или по телефону
"""

SYSTEM_PROMPT = f"""Ты — дружелюбный и профессиональный AI-ассистент интернет-магазина «Центр Красок #1».

Правила:
1. Отвечай ТОЛЬКО на основе базы знаний ниже. Не придумывай факты.
2. Если информации нет в базе знаний — скажи об этом и предложи позвонить: +7 778 061-50-00 или написать на info@centr-krasok.kz.
3. Будь вежлив и лаконичен. Используй эмодзи умеренно (1–2 на сообщение).
4. На вопросы не по теме магазина — вежливо перенаправляй к теме.
5. На вопросы об адресах и контактах — давай точные данные.

=== БАЗА ЗНАНИЙ ===
{COMPANY_KNOWLEDGE}
=== КОНЕЦ БАЗЫ ЗНАНИЙ ==="""

# ─── Инициализация Gemini (новая библиотека google-genai) ─────────────────────
client = genai.Client(api_key=GEMINI_KEY)

# История диалогов {user_id: [{"role": ..., "parts": [...]}]}
chat_histories: dict = {}


def get_ai_response(user_id: int, user_message: str) -> str:
    try:
        history = chat_histories.setdefault(user_id, [])

        # Добавляем сообщение пользователя в историю
        history.append(types.Content(role="user", parts=[types.Part(text=user_message)]))

        # Обрезаем историю до 20 сообщений
        if len(history) > 20:
            history[:] = history[-20:]

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1000,
                temperature=0.3,
            ),
        )

        answer = response.text

        # Сохраняем ответ модели в историю
        history.append(types.Content(role="model", parts=[types.Part(text=answer)]))

        return answer
    except Exception as e:
        logger.error("Ошибка Gemini API: %s", e)
        return "😔 Произошла техническая ошибка. Попробуйте позже или позвоните: +7 778 061-50-00"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text.strip()
    logger.info("Сообщение от %s (id=%s): %s", user.first_name, user.id, text)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = get_ai_response(user.id, text)
    await update.message.reply_text(reply)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_histories.pop(user.id, None)
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я AI-ассистент магазина «Центр Красок #1» 🎨\n\n"
        "Задайте любой вопрос:\n"
        "• Какие краски и бренды есть?\n"
        "• Где находятся магазины?\n"
        "• Как оформить заказ или доставку?\n"
        "• Условия для дизайнеров и строителей\n\n"
        "Просто напишите вопрос — я отвечу 💬"
    )


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_histories.pop(update.effective_user.id, None)
    await update.message.reply_text("🔄 История очищена. Начнём заново!")


def main() -> None:
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("reset", handle_reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
