from django.contrib import admin
from .models import Event, Registration, TelegramUser

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_time', 'end_time', 'created_by')
    list_filter = ('start_time', 'location')
    search_fields = ('title', 'description', 'location')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at')
    list_filter = ('event', 'registered_at')
    search_fields = ('user__username', 'event__title')

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_username', 'joined_at')
    search_fields = ('telegram_username', 'user__username')