describe('Get info about tournament entries', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR']

    frisby.create('Info about an entry')
        .get(API + 'tournament/ranking_test/entry/lisa')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes(
            {
                username: String,
                tournament_name: String,
                entry_id: Number
            }
        )
        .expectJSON(
            {
                username: 'lisa',
                tournament_name: 'ranking_test',
            }
        )
        .toss();

    frisby.create('A non-existent user')
        .get(API + 'tournament/ranking_test/entry/flubber')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Unknown player: flubber')
        .toss();
    frisby.create('malformed')
        .get(API + 'tournament/ranking_test/entry/lisa/a')
        .expectStatus(404)
        .toss();
});
