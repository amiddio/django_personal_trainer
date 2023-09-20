from django.test import TestCase
from trainer.models import Trainer
from trainer.services.service_trainer import ServiceTrainer


class ServiceTrainerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        Trainer.objects.create(name='name2', slug='name2', description='text', active=True)
        Trainer.objects.create(name='name3', slug='name3', description='text', active=True)
        Trainer.objects.create(name='name4', slug='name4', description='text', active=True)
        Trainer.objects.create(name='name5', slug='name5', description='text', active=False)

    def test_get_trainers_method(self):
        rows = ServiceTrainer.get_trainers()
        self.assertEquals(len(rows), 4)

    def test_get_random_trainers_method(self):
        rows4 = ServiceTrainer.get_random_trainers()
        rows2 = ServiceTrainer.get_random_trainers(number=2)
        self.assertEquals(len(rows4), 4)
        self.assertEquals(len(rows2), 2)

    def test_get_trainer_by_id_method(self):
        row = ServiceTrainer.get_trainer_by_id(trainer_id=1)
        self.assertEquals(row.name, 'name1')
        self.assertIsInstance(row, Trainer)
