from django.conf.urls import patterns, url

from admins import views


urlpatterns = patterns(
    '',
    # Control panels
    url(r'^admin/overview/$', views.overview, name='admin_overview'),

)
