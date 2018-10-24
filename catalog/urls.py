from django.urls import path

from .views import category, product, product_list


urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:slug>', category, name='category'),
    path('produto/<slug:slug>', product, name='product'),
]