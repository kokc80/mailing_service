from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientCreateView, MessageListView
from mailing.views import HomeView, MessageCreateView, MailingListView
from users.views import UsersListView

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recipient_list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient_create/",RecipientCreateView.as_view(), name="recipient_create"),
    path("mailings/all/", MailingListView.as_view(), name="mailings_list"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
]
