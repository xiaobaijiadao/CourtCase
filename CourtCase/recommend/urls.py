from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^search/$', views.index, name='recommend_search'),
    url(r'^list/$', views.list, name='recommend_list'),
    url(r'^searchbykey/$', views.list, name='search_list'),
    url(r'^display/(?P<case_id>[0-9a-z]+)$', views.display, name='recommend_display'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)