from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^tag/(?P<tag>[\w]+)', views.post_tagged, name='tagged'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
]
