from django.shortcuts import render


def index(request):
    context = {
        'title': 'django e-commerce'
    }
    return render(request, 'index.html', context)
