from django.contrib.auth.models import User
from django.test import TestCase
from taggit.models import Tag
from trainer.models import Trainer, Event
from trainer.services.service_event import ServiceEvent
from trainer.utils import TestMixin


class ServiceEventTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer1 = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        trainer2 = Trainer.objects.create(name='name2', slug='name2', description='text', active=True)
        User.objects.create_user(username='testuser1', password='12345')
        User.objects.create_user(username='testuser2', password='12345')
        tag1 = Tag.objects.create(name='yoga', slug='yoga')
        tag2 = Tag.objects.create(name='pilates', slug='pilates')
        cls.create_event(trainer1, name='Event name 1.1', timedelta_days=1, tags=tag1)
        cls.create_event(trainer1, name='Event name 1.2', timedelta_days=-1, tags=tag2)
        cls.create_event(trainer1, name='Event name 1.3', timedelta_days=2, tags=tag2)
        cls.create_event(trainer2, name='Event name 2.1', timedelta_days=1, tags=tag1)

    def test_get_events_method_without_args(self):
        rows = ServiceEvent.get_events()
        self.assertEquals(len(rows), 3)

    def test_get_events_with_limit(self):
        rows = ServiceEvent.get_events(limit=1)
        self.assertEquals(len(rows), 1)

    def test_get_events_with_trainer(self):
        trainer = Trainer.actived.get(pk=1)
        rows = ServiceEvent.get_events(trainer=trainer)
        self.assertEquals(len(rows), 2)

    def test_get_events_with_tags(self):
        tag = Tag.objects.get(pk=1)
        rows = ServiceEvent.get_events(tag_slug=tag)
        self.assertEquals(len(rows), 2)
        self.assertEquals(rows[0].name, 'Event name 1.1')
        self.assertEquals(rows[1].name, 'Event name 2.1')

    def test_get_event_by_id_method(self):
        row = ServiceEvent.get_event_by_id(event_id=1)
        self.assertEquals(row.name, 'Event name 1.1')
        self.assertIsInstance(row, Event)

    def test_add_user_to_event_method(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        ServiceEvent.add_user_to_event(event_id=1, user=user1)
        ServiceEvent.add_user_to_event(event_id=1, user=user2)
        row = ServiceEvent.get_event_by_id(event_id=1)
        self.assertEquals(len(row.user.all()), 2)
