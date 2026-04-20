from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.views.generic import DetailView, ListView, TemplateView
from mailing.models import Recipient, Message
from mailing.forms import RecipientForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# Create your views here.
# Recipient views
class RecipientListView(generic.ListView):
    model = Recipient
    template_name = "mailing/recipient_list.html"
    context_object_name = "recipients"


class RecipientDetailView(generic.DetailView):
    model = Recipient
    template_name = "recipient_detail.html"


class RecipientCreateView(generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_create.html"
    success_url = reverse_lazy("mailing:recipient_list")


# Message views
@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    """Отображение списка сообщений"""

    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_count()
        return context

    def get_count(self):
        messages = self.get_queryset()
        count = 0
        for message in messages:
            count += 1
        return count

    def get_queryset(self):
        queryset = cache.get("my_message_list")
        if not queryset:
            queryset = Message.objects.all()
            cache.set("my_message_list", queryset, 60 * 15)
        return queryset


class HomeView(generic.TemplateView):
    template_name = "home.html"

