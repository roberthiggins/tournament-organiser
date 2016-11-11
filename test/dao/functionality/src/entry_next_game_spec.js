var frisby = require('frisby'),
    tournament = 'next_game_test',
    API = process.env.API_ADDR + 'tournament/' + tournament + '/';

describe('Get the next game for an entry', function () {
    'use strict';
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(400)
        .expectBodyContains('Next game not scheduled. Check with the TO.')
        .toss();
});

describe('Get the next game for an entry', function () {
    'use strict';
    frisby.create('See next_game_test_player_5 next game (vs. player 4)')
        .get(API + 'entry/next_game_test_player_5/nextgame')
        .expectStatus(200)
        .expectJSONTypes({
            'table' : Number,
            'game_id': Number,
            'mission': String,
            'round': Number,
            'opponent': String
        })
        .expectJSON({
            'table'   : 2,
            'game_id' : Number,
            'mission' : 'TBA',
            'round'   : 2,
            'opponent': 'next_game_test_player_4'
        })
        .toss();
});
