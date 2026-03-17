from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import RecipientListView

app_name = MailingConfig.name

urlpatterns = [
#    path('', HomeView.as_view(), name='home'),
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
]