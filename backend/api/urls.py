from django.urls import path
from .views import upload_document, save_grundbuchdaten, list_all_bestandsverzeichnis, list_all_abteilung_2, abteilung2_mit_bestandsverzeichnis

urlpatterns = [
    path('upload-document/', upload_document, name='upload_document'),
    path('save-bestandsverzeichnis/', save_grundbuchdaten, name='save_bestandsverzeichnis'),
    path('bestandsverzeichnis-list-entries/', list_all_bestandsverzeichnis, name='list_entries'),
    path('abteilung-2-list-entries/', list_all_abteilung_2, name='list_abteilung_2'),
    path('abteilung2_mit_bestandsverzeichnis/', abteilung2_mit_bestandsverzeichnis)
]
