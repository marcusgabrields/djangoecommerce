from django.conf import settings
from django.shortcuts import render

from .forms import ContactForm


def index(request):
    return render(request, 'index.html')

def contact(request):
    succsess = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        succsess = True
    context = {
        'form': form,
        'success': succsess,
    }
    return render(request, 'contact.html', context)
