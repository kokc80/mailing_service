from django import forms

from .models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'fio', 'comment']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите e-mail:"})
        self.fields["fio"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ФИО:"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий:"})

# 20260417 проект4