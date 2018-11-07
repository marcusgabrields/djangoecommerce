from django.urls import path

from . import views

urlpatterns = [
    path('carrinho/adicionar/<slug:slug>', views.create_cartitem, name='create_cartitem')
]