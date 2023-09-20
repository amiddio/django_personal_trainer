from django.contrib import admin
from contact.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Настройки управления темой контактных сообщений"""

    list_display = ['title']
    ordering = ['title']
