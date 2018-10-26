from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContactForm


class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view()

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
