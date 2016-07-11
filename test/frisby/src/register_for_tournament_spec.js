describe('Test seeing and registering for a tournament', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR'];
    var entry = 'tournaments.?';

    frisby.create('See a list of tournaments')
        .get(API + 'tournament/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({tournaments: Array})
        .expectJSONTypes('tournaments.0',
            {
                date: String,
                name: String,
                rounds: Number
            }
        )
        .expectJSON('tournaments', [
            {date: '2095-06-01', name: 'northcon_2095',              rounds: 0},
            {date: '2095-07-02', name: 'entry_info_test',            rounds: 0},
            {date: '2095-07-03', name: 'entry_list_test',            rounds: 0},
            {date: '2095-07-04', name: 'entry_list_test_no_entries', rounds: 0},
            {date: '2095-07-05', name: 'category_test',              rounds: 0},
            {date: '2095-07-06', name: 'permission_test',            rounds: 0},
            {date: '2095-07-07', name: 'round_test',                 rounds: 0},
            {date: '1643-01-27', name: 'rank_test',                  rounds: 0},
            {date: '2095-08-12', name: 'next_game_test',             rounds: 4},
            {date: '2163-09-15', name: 'schedule_test',              rounds: 4},
            {date: '2095-07-01', name: 'mission_test',               rounds: 3}
        ])
        .toss();
});
