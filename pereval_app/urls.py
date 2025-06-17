from django.urls import path
from .views import SubmitDataView, PerevalDetailView


urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('submitData/<int:pk>/', PerevalDetailView.as_view(), name='pereval-detail'),
]
