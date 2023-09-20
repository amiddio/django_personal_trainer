from django.contrib.auth.models import User
from django.test import TestCase
from like_dislike.models import LikeDislike
from like_dislike.services.service_likedislike import ServiceLikeDislike
from trainer.models import Trainer


class ServiceLikeDislikeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Trainer.objects.create(name='name1', slug='name1', description='text', active=True)
        User.objects.create_user(username='testuser1', password='12345')

    def test_trainer_like(self):
        user = User.objects.get(pk=1)
        obj = ServiceLikeDislike.get_object_model(model=Trainer, pk=1)
        likedislike = ServiceLikeDislike(obj=obj, user=user, vote_type=LikeDislike.LIKE)
        likedislike.change_vote()
        like_count = obj.votes.like_count()
        dislike_count = obj.votes.dislike_count()
        self.assertEquals(like_count, 1)
        self.assertEquals(dislike_count, 0)

    def test_trainer_dislike(self):
        user = User.objects.get(pk=1)
        obj = ServiceLikeDislike.get_object_model(model=Trainer, pk=1)
        likedislike = ServiceLikeDislike(obj=obj, user=user, vote_type=LikeDislike.DISLIKE)
        likedislike.change_vote()
        like_count = obj.votes.like_count()
        dislike_count = obj.votes.dislike_count()
        self.assertEquals(like_count, 0)
        self.assertEquals(dislike_count, 1)

    def test_trainer_like_twice(self):
        user = User.objects.get(pk=1)
        obj = ServiceLikeDislike.get_object_model(model=Trainer, pk=1)
        likedislike = ServiceLikeDislike(obj=obj, user=user, vote_type=LikeDislike.LIKE)
        likedislike.change_vote()
        likedislike.change_vote()
        like_count = obj.votes.like_count()
        self.assertEquals(like_count, 0)

    def test_trainer_dislike_twice(self):
        user = User.objects.get(pk=1)
        obj = ServiceLikeDislike.get_object_model(model=Trainer, pk=1)
        likedislike = ServiceLikeDislike(obj=obj, user=user, vote_type=LikeDislike.DISLIKE)
        likedislike.change_vote()
        likedislike.change_vote()
        dislike_count = obj.votes.dislike_count()
        self.assertEquals(dislike_count, 0)

