from django.conf.urls import url
from . import views


app_name = 'survey'
urlpatterns = [
  #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index_view, name='index'),
  url(r'edit/$', views.edit_view, name='edit'),
  url(r'^login/$', views.login_view, name='login'),
  url(r'^logout/$', views.logout_view, name='logout'),
]
