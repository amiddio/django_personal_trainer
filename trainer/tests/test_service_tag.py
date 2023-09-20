from django.test import TestCase
from taggit.models import Tag
from trainer.services.service_tag import ServiceTag


class ServiceTagTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='yoga', slug='yoga')
        Tag.objects.create(name='pilates', slug='pilates')
        Tag.objects.create(name='calisthenics', slug='calisthenics')

    def test_get_all_method(self):
        rows = ServiceTag.get_all()
        self.assertEquals(len(rows), 3)

    def test_get_by_slug_method_if_success(self):
        row = ServiceTag.get_by_slug(slug='calisthenics')
        self.assertIsInstance(row, Tag)
        self.assertEquals(row.name, 'calisthenics')
