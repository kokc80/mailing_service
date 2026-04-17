from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientCreateView
from mailing.views import HomeView

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recipient_list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient_create/",RecipientCreateView.as_view(), name="recipient_create"), #????

]
