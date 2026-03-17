from django.shortcuts import render
from django.views import generic
from mailing.models import Recipient

# Create your views here.
class RecipientListView(generic.ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'
