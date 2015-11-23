# pylint: disable=C0111
from django.conf.urls import patterns, url

from public import public_views, views

# pylint: disable=C0103
urlpatterns = patterns('',

    # Public views
    url(r'^$', public_views.index, name='index'),
    url(r'^login$', public_views.login, name='login'),
    url(r'^signup$', public_views.create_account, name='create_account'),
    url(r'^tournament/(?P<tournament_id>.+)$',
        public_views.tournament, name='tournament'),
    url(r'^tournament/$',
        public_views.list_tournaments, name='apply_for_tournament'),
    url(r'^tournaments$',
        public_views.list_tournaments, name='list_tournaments'),

    # Logged in views
    url(r'^createtournament$',
        views.create_tournament, name='create_tournament'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^registerforatournament$',
        views.register_for_tournament, name='apply_for_tournament'),
    url(r'^suggestimprovement$',
        views.suggest_improvement, name='suggest_improvement'),
)
