from django.db import models

# Create your models here.
class Recipient(models.Model):
    email = models.CharField(max_length=20, verbose_name="E-mail", unique=True)
    fio = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return self.fio

    class Meta:
        ordering = ["email"]