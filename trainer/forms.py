from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма создания комментариев к странице тренера"""

    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={"rows": "3"}),
        }
