from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from .forms import ContactForm


User = get_user_model()

class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view()

def contact(request):
    succsess = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        succsess = True
    elif request.method == 'POST':
        messages.error(request, 'Formulario invalido')
    context = {
        'form': form,
        'success': succsess,
    }
    return render(request, 'contact.html', context)
