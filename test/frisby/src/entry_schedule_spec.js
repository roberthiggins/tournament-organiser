describe('See the schedule for an entry in a tournament', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('See lisa schedule')
        .get(URL + '/tournament/ranking_test/entry/lisa/schedule')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes('*', {
            'table' : Number,
            'game_id': Number,
            'round': Number,
            'opponent': String 
        })
        .expectJSON([
            {'table': 1, 'game_id': Number, 'round': 1, 'opponent': 'BYE'},
            {'table': 3, 'game_id': Number, 'round': 2, 'opponent': 'homer'}
        ])
        .toss();

    frisby.create('See homer schedule')
        .get(URL + '/tournament/ranking_test/entry/homer/schedule')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([
            {'table': 2, 'game_id': Number, 'round': 1, 'opponent': 'maggie'},
            {'table': 3, 'game_id': Number, 'round': 2, 'opponent': 'lisa'}
        ])
        .toss();

    frisby.create('Entry has not played a game')
        .get(URL + '/tournament/permission_test/entry/permission_test_player/schedule')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();

    frisby.create('No entry with that username')
        .get(URL + '/tournament/permission_test/entry/homer')
        .expectStatus(400)
        .toss();

    frisby.create('Tournament that does not exist')
        .get(URL + '/tournament/ranking_testdfsdfsdf/entry/lisa/schedule')
        .expectStatus(400)
        .toss();
});
