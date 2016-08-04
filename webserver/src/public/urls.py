# pylint: disable=missing-docstring
import os

from django.conf.urls import url
from django.views.generic import RedirectView

from public import public_views, views

NODE_URL = 'http://{}:{}'.format(
    os.environ['NODE_PORT_8000_TCP_ADDR'],
    os.environ['NODE_PORT_8000_TCP_PORT']
)

# pylint: disable=invalid-name
urlpatterns = [

    # Re-directs
    url(r'^createtournament$',
        RedirectView.as_view(url='{}/tournament/create'.format(NODE_URL)),
        name='create_tournament'),
    url(r'^devindex$', RedirectView.as_view(url='{}/devindex'.format(NODE_URL)),
        name='dev_index'),
    url(r'^logintonode$', RedirectView.as_view(url='{}/login'.format(NODE_URL)),
        name='login_to_node'),
    url(r'^feedback$',
        RedirectView.as_view(url='{}/feedback'.format(NODE_URL)),
        name='feedback'),

    # Public views
    url(r'^$', public_views.index, name='index'),
    url(r'^login$', public_views.login, name='login'),
    url(r'^rankings/(?P<tournament_id>.+)$',
        public_views.tournament_rankings, name='tournament_rankings'),
    url(r'^signup$', public_views.create_account, name='create_account'),
    url(r'^draw/(?P<tournament_id>.+)/(?P<round_id>.+)$',
        public_views.tournament_draw, name='draw'),
    url(r'^tournament/(?P<tournament_id>.+)$',
        public_views.tournament, name='tournament'),
    url(r'^tournament/$',
        public_views.list_tournaments, name='apply_for_tournament'),
    url(r'^tournaments$',
        public_views.list_tournaments, name='list_tournaments'),

    # Logged in views
    url(r'^enterscore/(?P<tournament_id>.+)/(?P<username>.+)$',
        views.enter_score, name='enter_score'),
    url(r'^entergamescore/(?P<t_id>.+)/(?P<user>.+)$',
        views.enter_score_for_game, name='enter_score_for_game'),
    url(r'^(?P<tournament_id>.+)/entries$',
        views.entry_list, name='tournament_entry_list'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^setcategories/(?P<tournament_id>.+)$',
        views.set_categories, name='set_categories'),
    url(r'^setmissions/(?P<tournament_id>.+)$',
        views.set_missions, name='set_missions'),
    url(r'^registerforatournament$',
        views.register_for_tournament, name='apply_for_tournament'),
    url(r'^setrounds/(?P<tournament_id>.+)$',
        views.set_rounds, name='set_rounds'),
]
