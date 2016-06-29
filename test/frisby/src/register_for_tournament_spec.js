describe('Test seeing and registering for a tournament', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('See a list of tournaments')
        .get(URL + '/tournament/')
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
        .expectJSON('tournaments.?',
            {
                date: '2095-06-01',
                name: 'northcon_2095',
                rounds: 0
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-06-01',
                name: 'southcon_2095',
                rounds: 0
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-10-31',
                name: 'conquest_2095',
                rounds: 0
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-10-10',
                name: 'painting_test',
                rounds: 0
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-08-12',
                name: 'ranking_test',
                rounds: 0
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-07-12',
                name: 'mission_test',
                rounds: 3
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-07-12',
                name: 'category_test',
                rounds: 3
            }
        )
        .expectJSON('tournaments.?',
            {
                date: '2095-07-12',
                name: 'permission_test',
                rounds: 0
            }
        )
        .toss();
});
