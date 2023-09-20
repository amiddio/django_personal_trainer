import datetime

from django.core.paginator import InvalidPage
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin
from trainer.models import Event, Comment


class TestMixin:
    """Вспомогательные методы для юниттестов"""

    @staticmethod
    def create_event(trainer, name='Event name', timedelta_days=1, active=True, tags=None):
        """Создается событие"""

        event = Event.objects.create(
            trainer=trainer,
            name=name,
            description='Event text',
            start=datetime.datetime.now(tz=timezone.utc) + timedelta(days=timedelta_days),
            end=datetime.datetime.now(tz=timezone.utc) + timedelta(days=timedelta_days, hours=1),
            price='10.00',
            total_places=3,
            active=active
        )
        if tags:
            event.tags.add(tags)

    @staticmethod
    def create_comment(trainer, user, active=True):
        """Создается комментарий"""

        Comment.objects.create(
            trainer=trainer,
            user=user,
            body='some comment',
            active=active
        )


class PaginateMixin:
    """Перегружаем методы пагинации"""

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            page_number = 1

        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(paginator.num_pages)

        return paginator, page, page.object_list, page.has_other_pages()


class AdminTrainerNameMixin:
    """Устанавливает имя тренера в модулях админки"""

    def get_trainer_name(self, object):
        return object.trainer.name

    get_trainer_name.short_description = 'Тренер'


@admin.action(description="Публиковать")
def make_published(modeladmin, request, queryset):
    """
    Действие админки.
    Позволяет на странице списка записей массово их публиковать"""
    queryset.update(active=True)


@admin.action(description="Скрыть")
def make_unpublished(modeladmin, request, queryset):
    """
    Действие админки.
    Позволяет на странице списка записей массово их скрывать"""
    queryset.update(active=False)


class AdminGeneralMixin:
    """Общие атрибуты моделей админки"""
    actions = (make_published, make_unpublished)
    save_on_top = True
