from django import forms
from django.core.exceptions import ValidationError

from .models import Recipient, Mailing, Message


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'fio', 'comment']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите e-mail:"})
        self.fields["fio"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ФИО:"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий:"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "recipients", "start_time", "end_time"]

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)
        super(MailingForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)

        self.fields["message"].widget.attrs.update({"class": "form-control", "placeholder": "Выберите сообщение"})

        self.fields["recipients"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите получателей"}
        )

        self.fields["start_time"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите дату и время начала отправки в формате YYYY-MM-DD HH:MM",
            }
        )

        self.fields["end_time"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите дату и время конца отправки в формате YYYY-MM-DD HH:MM",
            }
        )


    def clean(self):
        if not self.fields["start_time"] and not isinstance(self.fields["start_time"], datetime):
            raise ValidationError("Неправильный формат даты. Используйте формат YYYY-MM-DD HH:MM.")

        if not self.fields["end_time"] and not isinstance(self.fields["end_time"], datetime):
            raise ValidationError("Неправильный формат даты. Используйте формат YYYY-MM-DD HH:MM.")

        # if self.fields["start_time"] > self.fields["end_time"]:
        #     raise ValidationError("Время начала должно быть меньше времени окончания.")

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

