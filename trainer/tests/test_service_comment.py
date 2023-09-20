from django.contrib.auth.models import User
from django.test import TestCase
from trainer.models import Trainer, Comment
from trainer.services.service_comment import ServiceComment


class ServiceCommentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        user = User.objects.create_user(username='testuser1', password='12345')
        for i in range(5):
            Comment.objects.create(trainer=trainer, user=user, body=f'some comment {i}')

    def test_get_all_by_trainer_method(self):
        trainer = Trainer.actived.get(pk=1)
        rows1 = ServiceComment.get_all_by_trainer(trainer=trainer, page_number=1)
        rows2 = ServiceComment.get_all_by_trainer(trainer=trainer, page_number=2)
        self.assertEquals(len(rows1), 3)
        self.assertEquals(len(rows2), 2)

    def test_add_comment_method(self):
        trainer = Trainer.actived.get(pk=1)
        user = User.objects.get(pk=1)
        comment = Comment()
        comment.body = 'comment'
        ServiceComment.add_comment(comment=comment, trainer=trainer, user=user)
        rows = ServiceComment.get_all_by_trainer(trainer=trainer, page_number=2)
        self.assertEquals(len(rows), 3)
