from django.urls import path
from . import views

app_name = 'gpt'

urlpatterns = [
    path('', views.ask_question, name='ask'),
]

