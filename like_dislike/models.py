from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum


class LikeDislikeManager(models.Manager):
    """Вспомогательный менеджер с набором необходимых методов"""

    use_for_related_fields = True

    def like_count(self):
        """Возвращает количество лайков у записи"""

        return self.get_queryset().filter(vote__gt=0).count()

    def dislike_count(self):
        """Возвращает количество дизлайков у записи"""

        return self.get_queryset().filter(vote__lt=0).count()

    def sum_voting(self):
        """Возвращается сумма лайков/дизлайков"""

        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    """Универсальная модель для хранения Like/Dislike значений"""

    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Like'),
        (LIKE, 'Dislike')
    )

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeDislikeManager()
