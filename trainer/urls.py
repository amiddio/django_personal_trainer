from django.urls import path, reverse_lazy, include
from . import views
from .views import *

app_name = 'trainer'

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('trainers/', TrainerListView.as_view(), name='trainers-list'),
    path('trainer/<slug:slug>', TrainerDetailView.as_view(), name='trainer-detail'),
    path('book/', BookView.as_view(), name='event-book'),
    path('add_comment/', AddCommentView.as_view(), name='add-comment'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/', EventListView.as_view(), name='events-list'),
    path('events/tag/<slug:tag_slug>/', EventListView.as_view(), name='events-list-by-tag'),
]
