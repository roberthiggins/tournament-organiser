describe('Check Missions', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    // Normal behaviour
    frisby.create('POST 3 rounds to setup')
        .post(API + 'tournament/mission_test/rounds', {
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 missions to setup')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_1', 'mission_2', 'mission_3'])
        .toss();

    // set missions and then change numbe of rounds
    frisby.create('POST 3 rounds to setup')
        .post(API + 'tournament/mission_test/rounds', {
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 missions to setup')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_4', 'mission_5', 'mission_6']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'mission_6'])
        .toss();
    frisby.create('Add a 4th round')
        .post(API + 'tournament/mission_test/rounds', {
            numRounds: 4
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check 4th round is TBA')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'mission_6', 'TBA'])
        .toss();
    frisby.create('POST 2 rounds')
        .post(API + 'tournament/mission_test/rounds', {
            numRounds: 2
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 rounds')
        .post(API + 'tournament/mission_test/rounds', {
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check 3rd round is TBA and 4th is gone')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'TBA'])
        .toss();


    frisby.create('POST malformed missions')
        .post(API + 'tournament/not_real/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('POST malformed missions')
        .post(API + 'tournament/mission_test/missions', {}, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('Too few')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('Too many')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3', 'mission_4']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('None')
        .post(API + 'tournament/mission_test/missions', {
            missions: []
        }, {json: true})
        .expectStatus(400)
        .toss();
});
