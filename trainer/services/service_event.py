from django.contrib.auth.models import User
from django.db.models import Count, QuerySet, F
from trainer.models import Event, Trainer
from trainer.services.service_tag import ServiceTag


class ServiceEvent:

    # Количество записей на главной странице
    ROWS_HOME_LIMIT = 10

    # Количество записей на странице списка событий
    ROWS_LIMIT = 20

    @staticmethod
    def get_events(trainer: Trainer = None, limit: int = None, tag_slug: str = None) -> QuerySet[list[Event]]:
        """
        Возвращает список событий с различными видами фильтрации и условий
        :param trainer: Trainer
        :param limit: int
        :param tag_slug: str
        :return: QuerySet[list[Event]]
        """

        qs: QuerySet[list[Event]] = Event.actived.all() \
            .annotate(book_places=F('total_places') - Count('user')) \
            .order_by('start') \
            .select_related('trainer').prefetch_related('tags')
        if trainer:
            qs = qs.filter(trainer=trainer)
        if tag_slug:
            tag = ServiceTag.get_by_slug(slug=tag_slug)
            qs = qs.filter(tags__in=[tag])
        if limit:
            qs = qs[:limit]
        return qs

    @staticmethod
    def get_event_by_id(event_id: int) -> Event:
        """
        Возвращает событие по его id
        :param event_id: int
        :return: Event
        """

        return Event.actived.get(pk=event_id)

    @staticmethod
    def add_user_to_event(event_id: int, user: User) -> None:
        """
        Добавляет пользователя к событию
        :param event_id: int
        :param user: User
        :return: None
        """

        event = Event.actived.get(pk=event_id)
        event.user.add(user)
