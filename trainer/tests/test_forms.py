from django.test import TestCase
from trainer.forms import CommentForm


class CommentFormTest(TestCase):

    def test_comment_form_body_field_label(self):
        form = CommentForm()
        self.assertTrue(form.fields['body'].label == 'Комментарий')

    def test_form_comment_is_valid(self):
        form_data = {'body': 'text'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
