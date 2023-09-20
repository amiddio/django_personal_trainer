from captcha.fields import CaptchaField
from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from contact.models import Subject


class ContactForm(forms.Form):
    """Форма на странице контактов"""

    subject = forms.ModelChoiceField(queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    name = forms.CharField(label="Your name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()

    def send_email(self, data):
        """Отправка email-а"""

        try:
            msg_plain = render_to_string('contact/contact_email.txt', {'data': data})
            msg_html = render_to_string('contact/contact_email.html', {'data': data})
            send_mail(
                subject=data['subject'],
                message=msg_plain,
                from_email=data['email'],
                recipient_list=[settings.CONTACT_EMAIL],
                html_message=msg_html,
                fail_silently=False
            )
        except Exception:
            raise Exception("Internal server error! Your message cannot be send. Try it later.")
