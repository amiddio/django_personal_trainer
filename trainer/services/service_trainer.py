import random
from typing import Optional
from django.db.models import QuerySet
from trainer.models import Trainer


class ServiceTrainer:

    # Количество тренеров на странице списка тренеров
    ROWS_LIMIT = 4

    @staticmethod
    def get_trainers() -> QuerySet[list[Trainer]]:
        """
        Возвращает всех тренеров
        :return: QuerySet[list[Trainer]]
        """

        return Trainer.actived.all()

    @staticmethod
    def get_random_trainers(number: int = 4) -> Optional[QuerySet[list[Trainer]]]:
        """
        Возвращает определенное кол-во number случайных тренеров
        :param number: int
        :return: Optional[QuerySet[list[Trainer]]]
        """

        ids = Trainer.actived.all().values_list('pk', flat=True)
        if ids:
            ids = random.sample(set(ids), number)
            return Trainer.actived.all().filter(pk__in=ids)

    @staticmethod
    def get_trainer_by_id(trainer_id: int) -> Trainer:
        """
        Возвращает тренера по его id
        :param trainer_id:
        :return: Trainer
        """

        return Trainer.actived.get(pk=trainer_id)
