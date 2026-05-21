Telegram AI-бот «Центр Красок #1»
💬 Как работает бот
Команда / действие	Результат
`/start`	Приветствие + сброс истории
`/reset`	Очистить историю диалога
Любое текстовое сообщение	AI-ответ на основе данных о компании
Примеры вопросов, которые понимает бот:
Чем занимается компания?
Где находится магазин в Алматы?
Какие бренды красок есть?
Как оформить доставку?
Есть ли скидки для дизайнеров?
Сколько оттенков можно колеровать?
Как с вами связаться?
---
🏗️ Архитектура
```
bot.py
 ├── COMPANY\\\_KNOWLEDGE   — структурированная база знаний о компании
 ├── SYSTEM\\\_PROMPT       — инструкция для Claude (ограничивает "галлюцинации")
 ├── conversation\\\_history — история диалогов по user\\\_id (в памяти)
 ├── get\\\_ai\\\_response()   — вызов Claude API с историей контекста
 └── Handlers:
      ├── /start  → приветствие + сброс истории
      ├── /reset  → сброс истории
      └── text    → AI-ответ
```
Ключевые решения:
Контекст диалога — последние 10 пар сообщений хранятся на user
Защита от галлюцинаций — Claude работает строго в рамках `COMPANY\\\_KNOWLEDGE`
Graceful fallback — при отсутствии данных предлагает позвонить/написать
Typing action — бот показывает «печатает…» пока думает
---
☁️ Деплой (опционально)
На Railway.app (бесплатно):
Залейте код на GitHub
Подключите репозиторий на railway.app
Задайте переменные окружения `TELEGRAM\\\_TOKEN` и `ANTHROPIC\\\_KEY`
На VPS/сервере:
```bash
# Установить как systemd-сервис
sudo nano /etc/systemd/system/centr-krasok-bot.service
# \\\[Unit] Description=Centr Krasok Bot
# \\\[Service] ExecStart=/usr/bin/python3 /path/to/bot.py
#           Environment=TELEGRAM\\\_TOKEN=xxx ANTHROPIC\\\_KEY=xxx
# \\\[Install] WantedBy=multi-user.target
sudo systemctl enable --now centr-krasok-bot
