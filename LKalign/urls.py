from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from . import views
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# graph = os.path.join(BASE_DIR, 'lkalign', 'static', 'media')
# INDEX_ROOT = os.path.join(BASE_DIR, 'index')

app_name = 'lkalign'
urlpatterns = [
    # path('', views.FileFieldView.as_view(), name='lkalign'),
    # url(r'^aligns/(?P<path>.*)$', serve,
    #     {'document_root': graph, 'show_indexes': True},
    #     name='graph'
    #     ),
]