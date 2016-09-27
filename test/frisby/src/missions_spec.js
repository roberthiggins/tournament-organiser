describe('Check Missions', function () {
    'use strict';
    var frisby = require('frisby'),
        injector = require("./data_injector"),
        tournament = 'mission_test',
        API = process.env.API_ADDR;

    // Normal behaviour
    injector.postRounds(tournament, 3);
    injector.setMissions(tournament, ['mission_1', 'mission_2', 'mission_3']);
    frisby.create('Check those missions exist')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_1', 'mission_2', 'mission_3'])
        .toss();

    // set missions and then change number of rounds
    injector.postRounds(tournament, 4);
    frisby.create('Check 4th round is TBA')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_1', 'mission_2', 'mission_3', 'TBA'])
        .toss();
    injector.postRounds(tournament, 2);
    injector.postRounds(tournament, 3);
    frisby.create('Check 3rd round is TBA and 4th is gone')
        .get(API + 'tournament/mission_test/missions')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_1', 'mission_2', 'TBA'])
        .toss();


    frisby.create('POST missions as to')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('mission_test_to:password').toString("base64"))
        .expectStatus(200)
        .toss();
    frisby.create('POST missions as player')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('mission_test_player_1:password').toString("base64"))
        .expectStatus(403)
        .toss();
    frisby.create('POST missions as other')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('rank_test_player_1:password').toString("base64"))
        .expectStatus(403)
        .toss();
    frisby.create('POST missions with no auth')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .expectStatus(401)
        .toss();


    frisby.create('POST malformed missions')
        .post(API + 'tournament/not_real/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .toss();
    frisby.create('POST malformed missions')
        .post(API + 'tournament/mission_test/missions', {}, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .toss();
    frisby.create('Too few')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .toss();
    frisby.create('Too many')
        .post(API + 'tournament/mission_test/missions', {
            missions: ['mission_1', 'mission_2', 'mission_3', 'mission_4']
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .toss();
    frisby.create('None')
        .post(API + 'tournament/mission_test/missions', {
            missions: []
        }, {json: true})
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .toss();
});
