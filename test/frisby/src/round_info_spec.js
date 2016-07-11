describe('HTTP Method Test Suite', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR']

    frisby.create('POST 2 rounds to setup')
        .post(API + 'tournament/round_test/rounds', {
            numRounds: 2
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 2 missions to setup')
        .post(API + 'tournament/round_test/missions', {
            missions: ['mission_1', 'mission_2']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(API + 'tournament/round_test/rounds/1')
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: 'mission_1'
        })
        .toss();
    frisby.create('Check those missions exist')
        .get(API + 'tournament/round_test/rounds/2')
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: 'mission_2'
        })
        .toss();

    frisby.create('malformations')
        .get(API + 'tournament/foo/rounds/1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/4')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/-1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/1/rounds/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/round_test/rounds/1/1')
        .expectStatus(404)
        .toss();
    frisby.create('malformations')
        .get(API + 'tournament/1/rounds/1')
        .expectStatus(400)
        .toss();
});
