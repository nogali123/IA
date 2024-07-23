from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ajuste o nome da função aqui
]
