from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from . import views
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
graph = os.path.join(BASE_DIR, 'exelchange', 'static', 'media')
INDEX_ROOT = os.path.join(BASE_DIR, 'index')

app_name = 'exelchange'
urlpatterns = [
    path('', views.FileFieldView.as_view(), name='exelchange'),
    url(r'^graph/(?P<path>.*)$', serve,
        {'document_root': graph, 'show_indexes': True},
        name='graph'
        ),
]