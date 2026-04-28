from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.views.generic import DetailView, ListView, TemplateView, CreateView, View, DeleteView, UpdateView
from mailing.models import Recipient, Message, Mailing
from mailing.forms import RecipientForm, MailingForm
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from users.models import CustomUser
from .forms import MessageForm

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = "home.html"


class RecipientListView(generic.ListView):
    """Список получателей"""
    model = Recipient
    template_name = "mailing/recipient_list.html"
    context_object_name = "recipients"


class RecipientCreateView(generic.CreateView):
    """Добавление получателя"""
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_create.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(generic.UpdateView):
    """Редактирование получателя"""
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление получателя"""
    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def test_func(self):
        recipient = self.get_object()
        return self.request.user == recipient.owner


class MailingBreakAllView(View):
    """Отключение рассылок"""
    def post(self, request):
        mailings = Mailing.objects.all()
        for mailing in mailings:
            mailing.status_active = False
            print("Статус изменен")
            mailing.save()
        print("Рассылка выключена")
        return redirect("mailing:mailing_list")

cachetime1 = 10 # 60*5 1

@method_decorator(cache_page(cachetime1), name="dispatch")
class MailingView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Список рассылок основная страница"""
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get(self, request):
        mailings = self.get_user_mailings()
        recipients = self.get_user_recipients()
        active_mailings = mailings.filter(status="Запущена").count()

        if not self.request.user.groups.filter(name="Менеджер").exists():
            unique_recipients = recipients.filter(owner=self.request.user).count()
        else:
            unique_recipients = recipients.all().count()

        context = {
            "recipients": mailings,
            "total_mailings": mailings.count(),
            "active_mailings": active_mailings,
            "unique_recipients_count": unique_recipients,
            "is_manager": self.request.user.is_staff or self.request.user.groups.filter(name="Менеджер").exists(),
            "users_count": CustomUser.objects.all().count(),
        }
        return render(request, self.template_name, context)

    def get_user_mailings(self):
        """Получение рассылок пользователя"""
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=self.request.user)

    def get_user_subscribers(self):
        """Получение получателей пользователя"""
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Recipient.objects.all()
        else:
            return Recipient.objects.filter(owner=self.request.user)

    def test_func(self):
        return True


class MailingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Список рассылок"""
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджер").exists():
            queryset = Mailing.objects.all()
        else:
            queryset = Mailing.objects.filter(owner=self.request.user)
        return queryset

    def get_active_status(self):
        """Получение статуса возможности запуска рассылки"""
        mailings = self.get_queryset()
        active_status = True
        for mailing in mailings:
            active_status = mailing.status_active

        return active_status

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_count()
        context["is_manager"] = self.request.user.is_staff or self.request.user.groups.filter(name="Менеджер").exists()
        context["is_status_active"] = self.get_active_status()
        return context

    def get_count(self):
        """Получение количества рассылок"""
        mailings = self.get_queryset()
        if not mailings:
            return 0
        else:
            return mailings.count()

    def test_func(self):
        return True


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки"""

    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        # Логика для создания новой рассылки
        form = self.get_form()
        if form.is_valid():
            status_active = Mailing.objects.filter(
                status_active=True
            ).exists()  # Проверяем, есть ли активные рассылки
            new_mailing = form.save(commit=False)
            new_mailing.status_active = status_active
            new_mailing.owner = request.user
            new_mailing.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


@method_decorator(cache_page(cachetime1), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    """Подробная информация о сообщении"""

    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"

    def get_context_data(self, **kwargs):
        # Получаем контекст от родительского класса
        context = super().get_context_data(**kwargs)
        context["is_manager"] = (
                self.request.user.is_staff or self.request.user.groups.filter(name="Менеджеры").exists()
        )
        # Получаем сообщение из контекста
        message = self.object

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""
    model = Message
    template_name = "mailing/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление сообщения"""
    model = Message
    fields = ["subject", "body"]
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


@method_decorator(cache_page(cachetime1), name="dispatch")
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
        if messages is not None:
            count = 0
            for message in messages:
                count += 1
            return count

    def get_queryset(self):
       queryset = cache.get("my_message_list")
       if not queryset:
           queryset = Message.objects.all()
           cache.set("my_message_list", queryset, cachetime1)
           return queryset


class MessageDeleteView(generic.DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')