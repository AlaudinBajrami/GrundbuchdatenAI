from django.urls import path
from . import views

urlpatterns = [
    path('bestandsverzeichnis/', views.mock_bestandsverzeichnis),
    path('abteilung_2/', views.mock_abteilung_2),
]
