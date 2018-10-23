from django.urls import path

from .views import product_list, category


urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:slug>', category, name='category'),
]