from django.urls import path

from . import views

app_name = 'ChromoGraph'
urlpatterns = [
    path('', views.FileFieldView.as_view(), name='chromograph'),
]
