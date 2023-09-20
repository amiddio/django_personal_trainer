from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from trainer.models import Trainer, Comment


class VotesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        trainer = Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        user = User.objects.create_user(username='testuser1', password='12345')
        Comment.objects.create(trainer=trainer, user=user, body=f'some comment')

    def test_not_logged_in_user_vote(self):
        response = self.client.post(reverse('like_dislike:trainer-like'), {'pk': 1})
        self.assertEquals(response.status_code, 302)

    def test_not_exist_model_id_vote(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('like_dislike:trainer-like'), {'pk': 777})
        self.assertEquals(response.status_code, 500)

    def test_trainer_post_like(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('like_dislike:trainer-like'), {'pk': 1})
        self.assertEquals(response.status_code, 200)

    def test_trainer_post_dislike(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('like_dislike:trainer-dislike'), {'pk': 1})
        self.assertEquals(response.status_code, 200)

    def test_comment_post_like(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('like_dislike:comment-like'), {'pk': 1})
        self.assertEquals(response.status_code, 200)

    def test_comment_post_dislike(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('like_dislike:comment-dislike'), {'pk': 1})
        self.assertEquals(response.status_code, 200)
