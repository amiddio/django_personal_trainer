from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from taggit.models import Tag


class ServiceTag:

    @staticmethod
    def get_all() -> QuerySet[list[Tag]]:
        """
        Возвращает список всех тегов
        :return: QuerySet[list[Tag]]
        """

        return Tag.objects.all()

    @staticmethod
    def get_by_slug(slug: str) -> Tag:
        """
        Возвращает тег по его слагу
        :param slug: str
        :return: Tag
        """

        return get_object_or_404(Tag, slug=slug)
