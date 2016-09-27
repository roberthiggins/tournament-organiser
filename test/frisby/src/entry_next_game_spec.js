describe('Get the next game for an entry', function () {
    'use strict';
    var frisby = require('frisby'),
        tournament = 'next_game_test',
        API = process.env.API_ADDR + 'tournament/' + tournament + '/',
        injector = require("./data_injector");

    injector.postRounds(tournament, 2);
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(400)
        .expectBodyContains('Next game not scheduled. Check with the TO.')
        .toss();


    injector.postRounds(tournament, 4);
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({
            'table' : Number,
            'game_id': Number,
            'mission': String,
            'round': Number,
            'opponent': String
        })
        .expectJSON({
            'table'   : 1,
            'game_id' : Number,
            'mission' : 'TBA',
            'round'   : 3,
            'opponent': 'next_game_test_player_4'
        })
        .toss();
});
