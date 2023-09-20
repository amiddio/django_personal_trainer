from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from trainer.models import Trainer, Event, Comment
from trainer.utils import TestMixin


class TrainerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Trainer.objects.create(name='name1', slug='name1', description='text', active=True)

    def test_slug_is_unique(self):
        with self.assertRaises(IntegrityError):
            Trainer.objects.create(name='name2', slug='name1', description='text', active=False)

    def test_absolute_url(self):
        row = Trainer.actived.get(id=1)
        self.assertEquals(row.get_absolute_url(), '/trainer/name1')

    def test_get_actived_ordering(self):
        row = Trainer.actived.all()[0]
        self.assertEquals(row.name, 'name1')


class EventModelTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        cls.create_event(trainer, name='Event name 1', timedelta_days=1)
        cls.create_event(trainer, name='Event name 2', timedelta_days=-1)
        cls.create_event(trainer, name='Event name 3', timedelta_days=2)

    def test_get_actived_events(self):
        rows = Event.actived.all()
        self.assertEquals(len(rows), 2)
        self.assertEquals(rows[0].name, 'Event name 3')

    def test_absolute_url(self):
        row = Event.actived.get(pk=1)
        self.assertEquals(row.get_absolute_url(), '/event/1/')


class CommentModelTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        user1 = User.objects.create_user(username='testuser1', password='12345')
        user2 = User.objects.create_user(username='testuser2', password='12345')
        cls.create_comment(trainer=trainer, user=user1, active=True)
        cls.create_comment(trainer=trainer, user=user2, active=True)
        cls.create_comment(trainer=trainer, user=user1, active=False)

    def test_get_actived_ordering(self):
        row = Comment.actived.all()[0]
        user2 = User.objects.get(pk=2)
        self.assertEquals(row.user, user2)
