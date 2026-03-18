from django import forms

from .models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите e-mail:"})
        self.fields["fio"].widget.attrs.update({"class": "form-control", "placeholder": "Введите FIO:"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий:"})
