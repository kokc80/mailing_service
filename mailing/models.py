from django.db import models

# класс получателей
class Recipient(models.Model):
    email = models.CharField(max_length=20, verbose_name="E-mail", unique=True)
    fio = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return self.fio

    class Meta:
        ordering = ["email"]


# класс сообщений
class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


# class Mailing(models.Model):
#     STATUS_CHOICES = [
#         ('Создана', 'Создана'),
#         ('Запущена', 'Запущена'),
#         ('Завершена', 'Завершена')
#     ]
#     send_at models.DateTimeField(null=True, blank=True)
#     send_end_at models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Создана')
#     message  Сообщение(внешний ключ на модель «Сообщение»).
#     Получатели(«многие ко многим», связь с моделью «Получатель»).