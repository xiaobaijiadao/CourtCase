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
    url(r'^test/(?P<pwd>[0-9a-z]+)$', views.test),
    url(r'^testres/$', views.test_res_display, name='test_res'),
    url(r'^testres/caseP/$', views.case_p_display, name='caseP'),
    url(r'^testres/statuteP/$', views.statute_p_display, name='statuteP'),
    url(r'^testres/statuteR/$', views.statute_r_display, name='statuteR'),
    url(r'^testres/statutePR/$', views.statute_p_r_display, name='statutePR'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)