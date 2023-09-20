import logging

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import QuerySet
from trainer.models import Comment, Trainer

logger = logging.getLogger(__name__)


class ServiceComment:

    # Количество комментариев на детальной странице тренера
    ROWS_LIMIT = 3

    @staticmethod
    def get_all_by_trainer(trainer: Trainer, page_number: int) -> QuerySet[list[Trainer]]:
        """
        Возвращает комментарии к тренеру разбитые на страницы
        :param trainer: Trainer
        :param page_number: int
        :return: QuerySet[list[Trainer]]
        """

        qs = Comment.actived.all().filter(trainer=trainer).prefetch_related('user')
        paginator = Paginator(qs, ServiceComment.ROWS_LIMIT)
        return paginator.get_page(page_number)

    @staticmethod
    def add_comment(comment: Comment, trainer: Trainer, user: User) -> None:
        """
        Добавляет комментарий к странице тренера
        :param comment: Comment
        :param trainer: Trainer
        :param user: User
        :return: None
        """

        comment.trainer = trainer
        comment.user = user
        comment.save()

        logger.info(f'Пользователь {user} оставил сомментарий')
