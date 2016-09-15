describe('Get the next game for an entry', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR + 'tournament/next_game_test/',
        postRounds = function(numRounds){
            frisby.create('POST ' + numRounds + ' rounds to setup')
                .post(API + 'rounds', {
                    numRounds: numRounds
                }, {json: true})
                .addHeader('Authorization', "Basic " +
                    new Buffer('superuser:password').toString("base64"))
                .expectStatus(200)
                .toss();
        };

    postRounds(2);
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(400)
        .expectBodyContains('Next game not scheduled. Check with the TO.')
        .toss();


    postRounds(4);
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
