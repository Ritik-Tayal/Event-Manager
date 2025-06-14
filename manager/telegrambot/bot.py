from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from django.conf import settings
from event.models import Event, TelegramUser, Registration
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async



# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    if username:
        await sync_to_async(TelegramUser.objects.get_or_create)(
            telegram_username=username
        )
        await update.message.reply_text(
            f"👋 Hi @{username}, welcome to *EventHub Bot!*\n\n"
            "Here’s what I can do:\n"
            "• /link <your_django_username> – Link your Telegram to your account\n"
            "• /upcoming – Show upcoming events\n"
            "• /register <event_id> – Register for an event",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("❗ Please set a Telegram username in your Telegram settings to use this bot.")



# /upcoming command
async def upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = await sync_to_async(lambda: list(Event.objects.order_by('start_time')[:5]))()
    if events:
        msg = "📅 *Upcoming Events:*\n"
        for event in events:
            msg += f"\n• *{event.title}* — {event.start_time.strftime('%Y-%m-%d %H:%M')} at {event.location}"
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("There are no upcoming events right now.")



# /link command
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        django_username = context.args[0]
        telegram_username = update.effective_user.username

        if not telegram_username:
            await update.message.reply_text("❗ Please set a Telegram username before linking.")
            return

        user = await sync_to_async(User.objects.get)(username=django_username)
        await sync_to_async(TelegramUser.objects.update_or_create)(
            telegram_username=telegram_username,
            defaults={"user": user}
        )
        await update.message.reply_text(f"✅ Successfully linked to Django user: `{django_username}`", parse_mode='Markdown')

    except IndexError:
        await update.message.reply_text("❗ Usage: `/link <your_django_username>`", parse_mode='Markdown')
    except User.DoesNotExist:
        await update.message.reply_text("❌ No Django user found with that username.")



async def register_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_username = update.effective_user.username
        event_id = int(context.args[0])

        tg_user = await sync_to_async(TelegramUser.objects.get)(telegram_username=telegram_username)
        user = await sync_to_async(lambda: tg_user.user)()

        event = await sync_to_async(Event.objects.get)(id=event_id)

        _, created = await sync_to_async(Registration.objects.get_or_create)(
            user=user,
            event=event
        )

        if created:
            await update.message.reply_text(f"✅ Successfully registered for *{event.title}*!", parse_mode='Markdown')
        else:
            await update.message.reply_text("⚠️ You are already registered for this event.")
    except IndexError:
        await update.message.reply_text("❗ Usage: `/register <event_id>`", parse_mode='Markdown')
    except Event.DoesNotExist:
        await update.message.reply_text("❌ Event not found.")
    except TelegramUser.DoesNotExist:
        await update.message.reply_text("❌ You need to /link your account first.")



# Setup function for the application
def get_application():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("upcoming", upcoming))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CommandHandler("register", register_event))

    return app
