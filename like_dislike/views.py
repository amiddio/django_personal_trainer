from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from like_dislike.services.service_likedislike import ServiceLikeDislike


class VotesView(LoginRequiredMixin, View):
    """Представление которое обслуживает POST запросы добавления/удалений/изменения лайков/дизлайков
    на различные модели, типа Trainer, Comment и т.д."""

    model = None
    vote_type = None

    def handle_no_permission(self):
        if not self._is_ajax(self.request):
            return super().handle_no_permission()
        return JsonResponse({}, status=401)

    def post(self, request):
        try:
            obj = ServiceLikeDislike.get_object_model(model=self.model, pk=int(request.POST['pk']))
            ServiceLikeDislike(obj=obj, user=request.user, vote_type=self.vote_type).change_vote()
        except self.model.DoesNotExist:
            return JsonResponse({}, status=500)

        return JsonResponse({
            'like_count': obj.votes.like_count(),
            'dislike_count': obj.votes.dislike_count(),
        }, status=200)

    def _is_ajax(self, request):
        """Проверяем метод запроса на ajax"""

        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
