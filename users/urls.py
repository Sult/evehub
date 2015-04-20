from django.conf.urls import patterns, url

from users import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(
        r'^register/success/$',
        views.register_succes,
        name='register_success'
    ),

    url(r'^user/profile/$', views.profile, name='profile'),
    url(r'^user/membership/$', views.membership, name='membership'),

    # Control panels
)
