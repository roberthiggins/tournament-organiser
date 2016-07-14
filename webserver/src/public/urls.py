# pylint: disable=missing-docstring
from django.conf.urls import url

from public import public_views, views

# pylint: disable=invalid-name
urlpatterns = [

    # Public views
    url(r'^$', public_views.index, name='index'),
    url(r'^devindex$', public_views.dev_index, name='dev_index'),
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
    url(r'^createtournament$',
        views.create_tournament, name='create_tournament'),
    url(r'^enterscore/(?P<tournament_id>.+)/(?P<username>.+)$',
        views.enter_score, name='enter_score'),
    url(r'^entergamescore/(?P<t_id>.+)/(?P<user>.+)$',
        views.enter_score_for_game, name='enter_score_for_game'),
    url(r'^(?P<tournament_id>.+)/entries$',
        views.entry_list, name='tournament_entry_list'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^setcategories/(?P<tournament_id>.+)$',
        views.set_categories, name='set_categories'),
    url(r'^setmissions/(?P<tournament_id>.+)$',
        views.set_missions, name='set_missions'),
    url(r'^registerforatournament$',
        views.register_for_tournament, name='apply_for_tournament'),
    url(r'^setrounds/(?P<tournament_id>.+)$',
        views.set_rounds, name='set_rounds'),
    url(r'^suggestimprovement$',
        views.suggest_improvement, name='suggest_improvement'),
]
