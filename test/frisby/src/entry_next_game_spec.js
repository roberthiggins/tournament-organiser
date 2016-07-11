describe('Get the next game for an entry', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR'] + 'tournament/next_game_test/';

    frisby.create('Set next_game_test to 2 rounds')
        .post(API + 'rounds', {numRounds: 2})
        .expectBodyContains('Rounds set: 2')
        .expectStatus(200)
        .toss()
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON({})
        .toss();


    frisby.create('Set next_game_test to 4 rounds')
        .post(API + 'rounds', {numRounds: 4})
        .expectBodyContains('Rounds set: 4')
        .expectStatus(200)
        .toss()
    frisby.create('See next_game_test_player_3 next game (none)')
        .get(API + 'entry/next_game_test_player_3/nextgame')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({
            'table' : Number,
            'game_id': Number,
            'round': Number,
            'opponent': String 
        })
        .expectJSON(
            {
                'table'   : 1,
                'game_id' : Number,
                'round'   : 3,
                'opponent': 'next_game_test_player_4'}
        )
});
