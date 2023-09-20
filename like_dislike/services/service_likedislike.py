from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from like_dislike.models import LikeDislike


class ServiceLikeDislike:
    """Вспомогательный класс бизнес-логики между представлением и моделью"""

    def __init__(self, obj: models.Model, user: User, vote_type: int) -> None:
        self.obj = obj
        self.user = user
        self.vote_type = vote_type

    def change_vote(self) -> None:
        """
        Меняет состояние голоса (лайк/дизлайк). Голос создается, изменяется или удаляется
        :return: None
        """

        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(self.obj),
                object_id=self.obj.id,
                user=self.user
            )
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except LikeDislike.DoesNotExist:
            self.create()

    def create(self) -> None:
        """Добавляется голос в модель"""

        self.obj.votes.create(user=self.user, vote=self.vote_type)

    @staticmethod
    def get_object_model(model: models.Model, pk: int):
        """Возвращается объект модели для которой будет устанавливаться лайк/дизлайк"""

        return model.actived.get(pk=pk)
