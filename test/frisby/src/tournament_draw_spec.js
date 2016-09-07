describe('HTTP Method Test Suite', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('Check draw for tournament with no rounds')
        .get(API + 'tournament/category_test/rounds/1')
        .expectStatus(400)
        .expectBodyContains('Tournament category_test does not have a round 1')
        .toss();

    frisby.create('Setup some rounds for draw_test')
        .post(
            process.env.API_ADDR + 'tournament/draw_test/rounds',
            {numRounds: 2}
        )
        .expectStatus(200)
        .toss();
    frisby.create('Check the draw')
        .get(API + 'tournament/draw_test/rounds/1')
        .expectStatus(200)
        .expectJSON({
            draw: Array,
            mission: String
        })
        .toss();
});
