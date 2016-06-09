describe('Check Missions', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    // Normal behaviour
    frisby.create('POST 3 rounds to setup')
        .post(URL + '/setRounds', {
            tournamentId: 'mission_test',
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 missions to setup')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test',
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(URL + '/getMissions/mission_test')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_1', 'mission_2', 'mission_3'])
        .toss();

    // set missions and then change numbe of rounds
    frisby.create('POST 3 rounds to setup')
        .post(URL + '/setRounds', {
            tournamentId: 'mission_test',
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 missions to setup')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test',
            missions: ['mission_4', 'mission_5', 'mission_6']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(URL + '/getMissions/mission_test')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'mission_6'])
        .toss();
    frisby.create('Add a 4th round')
        .post(URL + '/setRounds', {
            tournamentId: 'mission_test',
            numRounds: 4
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check 4th round is TBA')
        .get(URL + '/getMissions/mission_test')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'mission_6', 'TBA'])
        .toss();
    frisby.create('POST 2 rounds')
        .post(URL + '/setRounds', {
            tournamentId: 'mission_test',
            numRounds: 2
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 3 rounds')
        .post(URL + '/setRounds', {
            tournamentId: 'mission_test',
            numRounds: 3
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check 3rd round is TBA and 4th is gone')
        .get(URL + '/getMissions/mission_test')
        .expectStatus(200)
        .expectJSONTypes('*', Array)
        .expectJSON(['mission_4', 'mission_5', 'TBA'])
        .toss();


    frisby.create('POST malformed missions')
        .post(URL + '/setMissions', {
            missions: ['mission_1', 'mission_2', 'mission_3']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('POST malformed missions')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test'
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('Too few')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test',
            missions: ['mission_1', 'mission_2']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('Too many')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test',
            missions: ['mission_1', 'mission_2', 'mission_3', 'mission_4']
        }, {json: true})
        .expectStatus(400)
        .toss();
    frisby.create('None')
        .post(URL + '/setMissions', {
            tournamentId: 'mission_test',
            missions: []
        }, {json: true})
        .expectStatus(400)
        .toss();
});