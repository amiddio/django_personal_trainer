from django.urls import path, reverse_lazy, include

from trainer.models import Trainer, Comment
from .models import LikeDislike
from .views import *

app_name = 'like_dislike'

urlpatterns = [
    path('trainer/like', VotesView.as_view(
        model=Trainer, vote_type=LikeDislike.LIKE), name='trainer-like'),
    path('trainer/dislike', VotesView.as_view(
        model=Trainer, vote_type=LikeDislike.DISLIKE), name='trainer-dislike'),
    path('comment/like', VotesView.as_view(
        model=Comment, vote_type=LikeDislike.LIKE), name='comment-like'),
    path('comment/dislike', VotesView.as_view(
        model=Comment, vote_type=LikeDislike.DISLIKE), name='comment-dislike'),
]
