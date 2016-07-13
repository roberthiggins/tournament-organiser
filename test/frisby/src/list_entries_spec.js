describe('Get a list of entries from a tournament', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('Details for existing tournament')
        .get(API + 'tournament/entry_list_test/entry/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes('*', String)
        .expectJSON([
            'entry_list_player',
            'entry_list_player_2'
        ])
        .toss();

    frisby.create('Tournament with no entries')
        .get(API + 'tournament/entry_list_test_no_entries/entry/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();

    frisby.create('Tournament that does not exist')
        .get(API + 'tournament/kdjflskdjflkdjflkdjf/entry/')
        .expectStatus(400)
        .toss();
});
