# 🎉 EventHub – Django Event Manager

A Django-based event management system that allows users to create, browse, and register for events. Features include user authentication, email confirmation via Celery, and Telegram bot integration.

---

## 🚀 Features

### ✅ Core Functionality
- User registration and login
- Create, browse, and register for events
- View your personal registrations

### ✅ Admin Features
- Admin dashboard for managing users and events
- Django admin panel with search and filters

### ✅ Integrations
- **Celery + Redis**: For sending registration confirmation emails asynchronously
- **Telegram Bot**:
  - `/start` – shows help
  - `/link <username>` – links Telegram account to Django user
  - `/upcoming` – lists upcoming events
  - `/register <event_id>` – register for events via Telegram

### ✅ Security
- Environment variables stored securely in `.env`
- Password hashing and Django-auth built-in protections

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2
- **Async Tasks**: Celery 5 + Redis
- **Database**: SQLite (or switch to PostgreSQL)
- **Bot Framework**: `python-telegram-bot`
- **Frontend**: Django Templates (with Bootstrap-ready base)

---