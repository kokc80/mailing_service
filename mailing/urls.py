from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    HomeView,
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView,
    MailingBreakAllView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, SendMailingView
)

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # рассылки
    path("mailings/break/", MailingBreakAllView.as_view(), name="mailing_break"),
    path("mailings/all/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # получатели
    path("recipient_list/", RecipientListView.as_view(), name="recipient_list"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path('recipients/update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    # сообщения
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('send-mailing/<int:mailing_id>/', SendMailingView.as_view(), name='send_mailing'),

]
