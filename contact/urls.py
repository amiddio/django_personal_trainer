from django.urls import path, include
from contact.views import ContactFormView, ContactThanksView

app_name = 'contact'

urlpatterns = [
    path('', ContactFormView.as_view(), name='form'),
    path('thanks/', ContactThanksView.as_view(), name='thanks'),
]
