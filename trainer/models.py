from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField
from datetime import datetime
from django.utils import timezone
from taggit.managers import TaggableManager
from like_dislike.models import LikeDislike


class ActivedManager(models.Manager):
    """Менеджер который фильтрует только активные (active=True) записи"""

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ActivedEventManager(models.Manager):
    """Менеджер возвращает только активные события.
    Это события у которых active=True и дата/время начала больше текущего времени"""

    def get_queryset(self):
        return super().get_queryset().filter(active=True).filter(start__gt=datetime.now(tz=timezone.utc))


class Trainer(models.Model):
    """Модель хранит информацию о тренерах"""

    name = models.CharField(max_length=50, verbose_name="Имя тренера", help_text="Имя и фамилия тренера")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг",
                            help_text="Уникальный постфикс тренера в урл-е")
    description = models.TextField(verbose_name="О тренере", help_text="Укажите краткую биографию тренера")
    avatar = ResizedImageField(size=[300, None], upload_to='trainers/%Y/%m/%d/', blank=True, null=True,
                               verbose_name="Фотография")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл",
                                 help_text="Флаг публикующий тренера на сайте")
    votes = GenericRelation(LikeDislike, related_query_name='trainers')

    objects = models.Manager()
    actived = ActivedManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Trainer {self.name}"

    def get_absolute_url(self):
        return reverse('trainer:trainer-detail', args=[self.slug])


class Event(models.Model):
    """Модель хранит информацию об событиях"""

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='events', verbose_name="Тренер")
    user = models.ManyToManyField(User, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=50, verbose_name="Название события")
    description = models.TextField(verbose_name="О событии")
    start = models.DateTimeField(verbose_name="Дата/время начала")
    end = models.DateTimeField(verbose_name="Дата/время окончания")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    total_places = models.PositiveSmallIntegerField(verbose_name="Количество мест")
    active = models.BooleanField(default=False, verbose_name="Вкл/Выкл",
                                 help_text="Флаг публикующий событие на сайте")
    tags = TaggableManager(verbose_name="Теги")

    objects = models.Manager()
    actived = ActivedEventManager()

    class Meta:
        ordering = ['-start']

    def __str__(self):
        return f"Event '{self.name}' of trainer '{self.trainer.name}'"

    def get_absolute_url(self):
        return reverse('trainer:event-detail', args=[self.pk])

    @property
    def booked(self):
        return self.user.count()


class Comment(models.Model):
    """Модель хранит информацию о комментариях пользователей к тренерам"""

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='comments', verbose_name="Тренер")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    body = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    active = models.BooleanField(default=True, verbose_name="Вкл/Выкл",
                                 help_text="Флаг публикующий комментарий на сайте")
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    objects = models.Manager()
    actived = ActivedManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Id #{self.pk} of {self.trainer}'
