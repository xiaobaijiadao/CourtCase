from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='recommend_index'),
    url(r'^list/$', views.list, name='recommend_list'),
    url(r'^display/$', views.display, name='recommend_display'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)