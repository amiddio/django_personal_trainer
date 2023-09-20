from django.db import models


class Subject(models.Model):
    """Модель для создания тем сообщений в форме контактов"""

    title = models.CharField(max_length=100, verbose_name="Тема сообщения")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
