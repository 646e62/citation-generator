from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('changelog/', views.changelog, name='changelog'),
    path('process_text/', views.process_text, name='process_text'),
#    path('<int:pk>/', views.changelog_detail, name='changelog_detail'),
]

