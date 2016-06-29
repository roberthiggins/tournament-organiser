describe('HTTP Method Test Suite', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('POST 2 rounds to setup')
        .post(URL + '/setRounds', {
            tournamentId: 'ranking_test',
            numRounds: 2
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('POST 2 missions to setup')
        .post(URL + '/tournament/ranking_test/missions', {
            missions: ['mission_1', 'mission_2']
        }, {json: true})
        .expectStatus(200)
        .toss();
    frisby.create('Check those missions exist')
        .get(URL + '/roundInfo/ranking_test/1')
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
        .get(URL + '/roundInfo/ranking_test/2')
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
        .get(URL + '/roundInfo/foo/1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/ranking_test/4')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/ranking_test/-1')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/ranking_test/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/1/ranking_test')
        .expectStatus(400)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/ranking_test/1/1')
        .expectStatus(404)
        .toss();
    frisby.create('malformations')
        .get(URL + '/roundInfo/1/1')
        .expectStatus(400)
        .toss();
});
