describe('Get info about tournament entries', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('Info about an entry')
        .get(API + 'tournament/entry_info_test/entry/entry_info_player')
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
                username: 'entry_info_player',
                tournament_name: 'entry_info_test',
            }
        )
        .toss();

    frisby.create('A non-existent user')
        .get(API + 'tournament/entry_info_test/entry/flubber')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Unknown player: flubber')
        .toss();
    frisby.create('malformed')
        .get(API + 'tournament/entry_info_test/entry/entry_info_player/a')
        .expectStatus(404)
        .toss();
});
