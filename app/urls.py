from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('changelog/', views.changelog, name='changelog'),
    path('process_text/', views.process_text, name='process_text'),
]

