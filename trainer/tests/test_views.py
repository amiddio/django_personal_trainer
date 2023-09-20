from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import TestCase
from trainer.models import Trainer, Event
from trainer.utils import TestMixin


class HomeViewTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_trainers = 4
        for trainer_n in range(number_of_trainers):
            trainer = Trainer.objects.create(name=f'name{trainer_n}', slug=f'name{trainer_n}',
                                             description='text', active=True)
            cls.create_event(trainer=trainer, timedelta_days=1)
            cls.create_event(trainer=trainer, timedelta_days=2)

    def test_view_home_page_is_exists(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_trainer_list_is_exist(self):
        resp = self.client.get('/')
        self.assertEqual(len(resp.context['trainers']), 4)

    def test_event_list_is_exist(self):
        resp = self.client.get('/')
        self.assertEqual(len(resp.context['events']), 8)


class TrainerListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_trainers = 7
        for trainer_n in range(number_of_trainers):
            Trainer.objects.create(name=f'name{trainer_n}', slug=f'name{trainer_n}', description='text', active=True)

    def test_view_url_exists_trainers_page(self):
        resp = self.client.get('/trainers/')
        self.assertEqual(resp.status_code, 200)

    def test_secont_page_of_trainers(self):
        resp = self.client.get('/trainers/?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_not_exist_page_number_of_trainers(self):
        resp = self.client.get('/trainers/?page=200')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page_obj'].number, 2)

    def test_page_is_not_number_of_trainers(self):
        resp = self.client.get('/trainers/?page=qwerty')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page_obj'].number, 1)

    def test_paginate_is_four(self):
        resp = self.client.get('/trainers/')
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(len(resp.context['trainers']), 4)


class TrainerDetailViewTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        Trainer.objects.create(name='name1', slug='name1', description='text', active=True)

    def test_trainer_detail_page_is_exist(self):
        resp = self.client.get('/trainer/name1')
        self.assertEqual(resp.status_code, 200)

    def test_events_list_exist(self):
        trainer = Trainer.actived.get(id=1)
        self.create_event(trainer)
        self.create_event(trainer, timedelta_days=2)
        resp = self.client.get('/trainer/name1')
        self.assertTrue(resp.context['event_list'])
        self.assertEqual(len(resp.context['event_list']), 2)

    def test_comments_list_exist(self):
        trainer = Trainer.actived.get(id=1)
        user = User.objects.create_user(username='testuser1', password='12345')
        self.create_comment(trainer=trainer, user=user)
        self.create_comment(trainer=trainer, user=user)
        self.create_comment(trainer=trainer, user=user)
        resp = self.client.get('/trainer/name1')
        self.assertTrue(resp.context['page_obj'])
        self.assertEqual(len(resp.context['page_obj']), 3)


class EventListViewTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        cls.create_event(trainer=trainer, timedelta_days=1)
        cls.create_event(trainer=trainer, timedelta_days=2)
        cls.create_event(trainer=trainer, timedelta_days=3)
        cls.create_event(trainer=trainer, timedelta_days=-1)
        cls.create_event(trainer=trainer, timedelta_days=4, active=False)

    def test_event_list_page_is_exist(self):
        resp = self.client.get('/events/')
        self.assertEqual(resp.status_code, 200)

    def test_events_list(self):
        resp = self.client.get('/events/')
        self.assertEqual(len(resp.context['events']), 3)


class EventDetailViewTest(TestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        cls.create_event(trainer=trainer, timedelta_days=1)
        User.objects.create_user(username='testuser1', password='12345')

    def test_event_detail_page_is_exist(self):
        resp = self.client.get('/event/1/')
        self.assertEqual(resp.status_code, 200)

    def test_event_book(self):
        user = User.objects.get(id=1)
        event = Event.actived.get(id=1)
        self.client.login(username='testuser1', password='12345')
        data = {
            'user_id': 1,
            'event_id': 1,
        }
        resp = self.client.post('/book/', data)
        self.assertEqual(resp.status_code, 302)
        self.assertIsInstance(resp, HttpResponseRedirect)
