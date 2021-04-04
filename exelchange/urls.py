from django.urls import path
from . import views

app_name = 'exelchange'
urlpatterns = [
    path('', views.FileFieldView.as_view(), name='exelchange'),
]