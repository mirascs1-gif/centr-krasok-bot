"""
Telegram AI-бот для «Центр Красок #1»
======================================
Запуск:
    pip install python-telegram-bot anthropic
    python bot.py

Переменные окружения (или задайте прямо здесь):
    TELEGRAM_TOKEN  — 8808605575:AAHqbozqgBNqAz5hkeGm9vcguuTdXgz9c0Y
    ANTHROPIC_KEY   — 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
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import anthropic

# ─── Настройка логгера ────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── Токены (замените своими или выставьте переменные окружения) ──────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8808605575:AAHqbozqgBNqAz5hkeGm9vcguuTdXgz9c0Y")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY", "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")
 
# ─── База знаний о компании ────────────────────────────────────────────────────
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
- Instagram: https://www.instagram.com/centr_krasok/
- Facebook:  https://www.facebook.com/profile.php?id=100075230594445
- YouTube:   https://www.youtube.com/channel/UCPC7__jM5FzQXQOgqsNbUlQ

## Ассортимент (категории товаров)
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
Masterline и другие.
Страны: Италия, Франция, Великобритания, Нидерланды, США и др.

## Ключевые преимущества
- Более 45 000 оттенков колеровки
- Более 20 брендов и 40+ марок в ассортименте
- Сертифицированная и экологически чистая продукция (рекомендована для детских и
  лечебных учреждений)
- Бесплатная консультация специалистов
- Доставка курьером или самовывоз из шоу-рума
- Акции, скидки и программа лояльности
- Сервис подбора цвета и онлайн-каталог

## Для профессионалов
- Партнёрская программа для дизайнеров: скидки, бонусы, участие в программе лояльности,
  консультации экспертов. Подробнее: https://centr-krasok.kz/designers/
- Условия для строителей: https://centr-krasok.kz/for_builders/
- Корпоративным клиентам — особые условия.

## Клиенты (компании, которым доверяют)
МАСП, Casa Azzurra, Mossebo, Pinteriors, Alyer, One Space, Shafran, Шатура,
Umtyl edu, Rams City, Four Seasons, Центр Декора, Cappuccino, Desso, INTHAI,
Mega, Salvare, YA, mig и другие.

## Доставка и оплата
- Доставка: курьерская (до двери) или самовывоз из шоу-рума Алматы / Астана
- Оплата: Visa, Mastercard, Kaspi Pay
- Оформление заказа: через сайт или по телефону

## Дополнительные сервисы
- Онлайн-каталог с остатками по городам
- Сканер штрихкода для быстрого поиска товара
- Подбор цвета и колеровка на месте
- Раздел «Вдохновение» с идеями интерьеров
- Глоссарий терминов
- Статьи и новости о тенденциях отделки (например, цветовые тренды AkzoNobel 2026)
"""

# ─── Системный промпт ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""Ты — дружелюбный и профессиональный AI-ассистент интернет-магазина «Центр Красок #1».

Правила работы:
1. ОТВЕЧАЙ ТОЛЬКО на основе базы знаний, приведённой ниже. Не придумывай факты.
2. Если информации нет в базе знаний — честно скажи об этом и предложи позвонить
   по телефону +7 778 061-50-00 или написать на info@centr-krasok.kz.
3. Будь вежлив, лаконичен и по делу. Используй эмодзи умеренно (1–2 на сообщение).
4. Не отвечай на вопросы, не связанные с компанией или красками/отделкой.
   Вежливо перенаправь пользователя к теме магазина.
5. При ответе на вопросы об адресах, контактах, режиме работы — давай точные данные.
6. Поддерживай контекст диалога — учитывай предыдущие сообщения пользователя.

=== БАЗА ЗНАНИЙ ===
{COMPANY_KNOWLEDGE}
=== КОНЕЦ БАЗЫ ЗНАНИЙ ===
"""

# ─── Хранилище истории диалогов (в памяти, по user_id) ────────────────────────
# Формат: {user_id: [{"role": "user"/"assistant", "content": "..."}]}
conversation_history: dict[int, list[dict]] = {}
MAX_HISTORY = 10  # максимум пар сообщений на пользователя

# ─── Инициализация клиента Anthropic ──────────────────────────────────────────
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)


def get_ai_response(user_id: int, user_message: str) -> str:
    """Отправляет сообщение в Claude и возвращает ответ."""
    history = conversation_history.setdefault(user_id, [])

    # Добавляем сообщение пользователя
    history.append({"role": "user", "content": user_message})

    # Обрезаем историю до MAX_HISTORY пар (2*MAX_HISTORY сообщений)
    if len(history) > MAX_HISTORY * 2:
        history[:] = history[-(MAX_HISTORY * 2):]

    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=history,
        )
        answer = response.content[0].text

        # Сохраняем ответ в историю
        history.append({"role": "assistant", "content": answer})
        return answer

    except anthropic.APIError as e:
        logger.error("Ошибка Anthropic API: %s", e)
        return (
            "😔 Произошла техническая ошибка. Пожалуйста, попробуйте позже "
            "или позвоните нам: +7 778 061-50-00"
        )


# ─── Обработчики Telegram ──────────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает любое текстовое сообщение от пользователя."""
    user = update.effective_user
    text = update.message.text.strip()

    logger.info("Сообщение от %s (id=%s): %s", user.first_name, user.id, text)

    # Отображаем «печатает…»
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    reply = get_ai_response(user.id, text)
    await update.message.reply_text(reply)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение при /start."""
    user = update.effective_user
    # Сбрасываем историю при старте
    conversation_history.pop(user.id, None)

    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я AI-ассистент магазина «Центр Красок #1» 🎨\n\n"
        "Задайте любой вопрос о нашем магазине:\n"
        "• Какие краски и бренды есть?\n"
        "• Где находятся магазины?\n"
        "• Как оформить заказ или доставку?\n"
        "• Условия для дизайнеров и строителей\n"
        "• И многое другое!\n\n"
        "Просто напишите вопрос — я отвечу 💬"
    )


async def handle_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /reset — очищает историю диалога."""
    conversation_history.pop(update.effective_user.id, None)
    await update.message.reply_text("🔄 История диалога очищена. Начнём заново!")


# ─── Точка входа ──────────────────────────────────────────────────────────────
def main() -> None:
    import asyncio
    from telegram.ext import CommandHandler

    # Фикс для Python 3.12+ / 3.14 на Windows
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("reset", handle_reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
