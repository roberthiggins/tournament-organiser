describe('Getting tournament information', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR,
        injector = require('./data_injector');

    injector.createTournament('northcon_2095', '2095-06-01');

    frisby.create('Details for existing tournament')
        .get(API + 'tournament/northcon_2095')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON({
            date: '2095-06-01',
            name: 'northcon_2095',
            rounds: 0
        })
        .toss();

    frisby.create('Non-existent tournament')
        .get(API + 'tournament/not_a_tournament')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Tournament not_a_tournament not found in database')
        .toss();
});
