SELECT setup_permissions();

SELECT half_tournament_test_setup('next_game_test', '2095-08-12');
SELECT half_tournament_test_setup('rank_test', '1643-01-27');
SELECT half_tournament_test_setup('schedule_test', '2163-09-15');
SELECT half_tournament_test_setup('draw_test', '1985-01-27');

SELECT create_user('superuser', TRUE);
