from django.contrib import admin

from mailing.models import Recipient


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "fio", "comment")
