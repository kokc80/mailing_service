from django.shortcuts import render
from django.views import generic
from mailing.models import Recipient, Message
from mailing.forms import RecipientForm
from django.urls import reverse_lazy

# Create your views here.
# Recipient views
class RecipientListView(generic.ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"


class RecipientDetailView(generic.DetailView):
    model = Recipient
    template_name = "recipient_detail.html"


class RecipientCreate(generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_create.html"
    success_url = reverse_lazy("mailing:recipient_list")


# Message views
class MessageList(generic.ListView):
    model = Message
    template_name = "message_list.html"


class HomeView(generic.TemplateView):
    template_name = "home.html"

