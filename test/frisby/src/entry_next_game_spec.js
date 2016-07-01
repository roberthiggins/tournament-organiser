describe('Get the next game for an entry', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('Set ranking_test to 2 rounds')
        .post(URL + '/tournament/ranking_test/rounds', {numRounds: 2})
        .expectBodyContains('Rounds set: 2')
        .expectStatus(200)
        .toss()
    frisby.create('See lisa next game (none)')
        .get(URL + '/tournament/ranking_test/entry/lisa/nextgame')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON({})
        .toss();


    frisby.create('Set ranking_test to 4 rounds')
        .post(URL + '/tournament/ranking_test/rounds', {numRounds: 4})
        .expectBodyContains('Rounds set: 4')
        .expectStatus(200)
        .toss()
    frisby.create('See lisa next game (none)')
        .get(URL + '/tournament/ranking_test/entry/lisa/nextgame')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({
            'table' : Number,
            'game_id': Number,
            'round': Number,
            'opponent': String 
        })
        .expectJSON(
            {'table': 1, 'game_id': Number, 'round': 3, 'opponent': 'bart'}
        )
});
