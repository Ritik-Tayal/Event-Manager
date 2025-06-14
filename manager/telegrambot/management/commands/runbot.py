from django.core.management.base import BaseCommand
from telegrambot.bot import get_application

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        app = get_application()
        app.run_polling()
