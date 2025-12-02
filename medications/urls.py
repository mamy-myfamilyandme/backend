from django.urls import path
from .views import process_prescription_view

urlpatterns = [
    path('upload/', process_prescription_view, name='upload_prescription'),
]
