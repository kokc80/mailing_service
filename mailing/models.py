from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser
from datetime import datetime, time, timezone




# модель получателей
class Recipient(models.Model):
    email = models.CharField(max_length=20, verbose_name="E-mail", unique=True)
    fio = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="recipient_owner", default=1)

    def __str__(self):
        return self.fio

    class Meta:
        ordering = ["email"]


# модель сообщений
class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время последнего обновления")

    def __str__(self):
        return self.subject


# модель рассылки
class Mailing(models.Model):
    """Модель «Рассылка»"""
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]


    def get_default_start_time(self):
        return timezone.make_aware(datetime.combine(timezone.now().date(), time(12, 0)))


    def get_default_end_time(self):
        return timezone.make_aware(datetime.combine(timezone.now().date(), time(22, 0)))


    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailing",
    )
    recipients = models.ManyToManyField(Recipient, related_name="recipients", verbose_name="Получатели")
    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки", blank=False, null=False)
    first_sent_at = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки", blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Создана", verbose_name="Статус")

    status_active = models.BooleanField(verbose_name="Возможность рассылки", default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="mailingr", default=1)


    def save(self, *args, **kwargs):
        self.clean()
        if self.pk is None:
            self.status_active = Mailing.objects.filter(status_active=True).exists()

        super().save(*args, **kwargs)


    def clean(self):
        if not self.start_time and not isinstance(self.start_time, datetime):
            raise ValidationError("Неправильный формат даты. Используйте формат YYYY-MM-DD HH:MM.")

        if not self.end_time and not isinstance(self.end_time, datetime):
            raise ValidationError("Неправильный формат даты. Используйте формат YYYY-MM-DD HH:MM.")

        if self.start_time >= self.end_time:
            raise ValidationError("Время начала должно быть меньше времени окончания.")


    def update_status(self):
        now = timezone.now()
        if self.status_active is True:
            if now < self.start_time:
                new_status = "Создана"
            elif self.start_time <= now <= self.end_time:
                new_status = "Запущена"
            else:
                new_status = "Завершена"

            if self.status != new_status:
                self.status = new_status
                self.save(update_fields=["status"])
        else:
            raise ValidationError("Невозможно запустить рассылку")


    def __str__(self):
        return f"Рассылка с {self.start_time} до {self.end_time} - Статус: {self.status}"


    def is_completed(self):
        return self.status == "Завершена"
