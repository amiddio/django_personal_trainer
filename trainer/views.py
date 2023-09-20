from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from trainer.forms import CommentForm
from trainer.models import Trainer, Event
from trainer.services.service_comment import ServiceComment
from trainer.services.service_event import ServiceEvent
from trainer.services.service_tag import ServiceTag
from trainer.services.service_trainer import ServiceTrainer
from trainer.utils import PaginateMixin


class HomeView(TemplateView):
    """Главная страница"""

    template_name = 'trainer/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainers'] = ServiceTrainer.get_random_trainers()
        context['events'] = ServiceEvent.get_events(limit=ServiceEvent.ROWS_HOME_LIMIT)
        return context


class TrainerListView(PaginateMixin, ListView):
    """Страница с списком тренеров"""

    model = Trainer
    template_name = 'trainer/trainers.html'
    queryset = ServiceTrainer.get_trainers()
    context_object_name = 'trainers'
    paginate_by = ServiceTrainer.ROWS_LIMIT


class TrainerDetailView(DetailView):
    """Детальная страница тренера"""

    model = Trainer
    template_name = 'trainer/trainer_detail.html'
    context_object_name = 'trainer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_list'] = ServiceEvent.get_events(trainer=self.object)
        context['form'] = CommentForm()
        context['page_obj'] = ServiceComment.get_all_by_trainer(
            trainer=self.object,
            page_number=self.request.GET.get('page')
        )
        return context


class EventListView(ListView):
    """Страница списка событий"""

    model = Event
    template_name = 'trainer/events.html'
    context_object_name = 'events'
    paginate_by = ServiceEvent.ROWS_LIMIT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = ServiceTag.get_all()
        return context

    def get_queryset(self):
        return ServiceEvent.get_events(tag_slug=self.kwargs.get('tag_slug', None))


class EventDetailView(DetailView):
    """Детальная страница события"""

    model = Event
    template_name = 'trainer/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Event.actived.all().filter(pk=pk).prefetch_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.book_places = self.object.total_places - self.object.user.count()
        return context


class BookView(View):
    """Бронирование события. Методом POST пользователь подписывается на событие"""

    def post(self, request):
        user_id = int(request.POST.get('user_id', 0))
        event_id = int(request.POST.get('event_id', 0))
        if not user_id or not event_id or request.user.id != user_id:
            raise ValueError("Incorrect booking data")

        ServiceEvent.add_user_to_event(event_id=event_id, user=request.user)
        event = ServiceEvent.get_event_by_id(event_id=event_id)
        messages.success(request, f"You successfully booked on - {event}")

        return HttpResponseRedirect(request.POST.get('next', '/'))


class AddCommentView(FormView):
    """Добавление комментария тренеру"""

    form_class = CommentForm
    trainer = None

    def get_success_url(self):
        if self.trainer:
            return reverse('trainer:trainer-detail', args=[self.trainer.slug])
        else:
            return reverse('trainer:trainers-list')

    def form_valid(self, form):
        self.trainer = ServiceTrainer.get_trainer_by_id(
            trainer_id=self.request.POST.get('trainer_id')
        )
        if not self.trainer:
            messages.error(self.request, "Cannot added comment. Trainer isn't choosed.")
        else:
            ServiceComment.add_comment(
                comment=form.save(commit=False),
                trainer=self.trainer,
                user=self.request.user
            )
            messages.success(self.request, "Your comment successfully added")

        return super().form_valid(form)
