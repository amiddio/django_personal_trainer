from django.contrib import admin
from django.utils.safestring import mark_safe
from trainer.models import Trainer, Event, Comment
from trainer.utils import AdminTrainerNameMixin, AdminGeneralMixin


@admin.register(Trainer)
class TrainerAdmin(AdminGeneralMixin, admin.ModelAdmin):
    """Настройки управления тренеров"""

    list_display = ('name', 'slug', 'get_html_photo', 'active')
    fields = ('id', 'name', 'slug', 'description', 'avatar', 'get_html_photo', 'active')
    readonly_fields = ('id', 'get_html_photo')
    prepopulated_fields = {'slug': ('name', )}

    def get_html_photo(self, object):
        """Возвращает миниатюру аватара тренера"""
        if object.avatar:
            return mark_safe(f'<img src="{object.avatar.url}" width="50">')

    get_html_photo.short_description = "Фотография"


@admin.register(Event)
class EventAdmin(AdminGeneralMixin, AdminTrainerNameMixin, admin.ModelAdmin):
    """Настройки управления событиями"""

    list_display = ('get_trainer_name', 'name', 'start', 'end', 'get_booked_property', 'total_places', 'active')
    fields = ('id', 'trainer', 'user', 'get_booked_property', 'name', 'description',
              'start', 'end', 'price', 'total_places', 'active', 'tags')
    readonly_fields = ('id', 'get_booked_property')
    list_filter = ('start', 'active')
    filter_horizontal = ('user',)

    def get_booked_property(self, object):
        """Возвращает кол-во забронированых на событие пользователей"""
        return object.booked

    get_booked_property.short_description = 'Забронировано'


@admin.register(Comment)
class CommentAdmin(AdminGeneralMixin, AdminTrainerNameMixin, admin.ModelAdmin):
    """Настройки управления комментариями к тренерам"""

    list_display = ('get_trainer_name', 'user', 'created', 'active')
    fields = ('id', 'trainer', 'user', 'body', 'active', 'created')
    readonly_fields = ('id', 'created')
    list_filter = ('active', 'created')
