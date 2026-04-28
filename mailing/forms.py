from django import forms


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


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

