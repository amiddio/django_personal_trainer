from django.views.generic import FormView, TemplateView
from contact.forms import ContactForm


class ContactFormView(FormView):
    """Представление формы контактов"""

    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = "thanks"

    def form_valid(self, form):
        try:
            form.send_email(data=form.cleaned_data)
            return super().form_valid(form=form)
        except Exception as e:
            form.add_error(None, str(e))
            return super().form_invalid(form=form)


class ContactThanksView(TemplateView):
    """Представление успешной отправки формы"""

    template_name = "contact/thanks.html"
