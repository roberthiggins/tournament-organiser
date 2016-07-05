describe('See the schedule for an entry in a tournament', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR']

    frisby.create('See lisa schedule')
        .get(API + 'tournament/ranking_test/entry/lisa/schedule')
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

    frisby.create('Set homer schedule to 8 rounds')
        .post(API + 'tournament/ranking_test/rounds', {numRounds: 4})
        .expectBodyContains('Rounds set: 4')
        .expectStatus(200)
        .toss()
    frisby.create('See homer schedule')
        .get(API + 'tournament/ranking_test/entry/homer/schedule')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([
            {"game_id": Number, "table": 2, "round": 1, "opponent": "maggie"},
            {"game_id": Number, "table": 3, "round": 2, "opponent": "lisa"},
            {"game_id": Number, "table": 3, "round": 3, "opponent": "BYE"},
            {"game_id": Number, "table": 3, "round": 4, "opponent": "bart"}
        ])
        .toss();

    frisby.create('Entry has not played a game')
        .get(API + 'tournament/permission_test/entry/permission_test_player/schedule')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();

    frisby.create('No entry with that username')
        .get(API + 'tournament/permission_test/entry/homer')
        .expectStatus(400)
        .toss();

    frisby.create('Tournament that does not exist')
        .get(API + 'tournament/ranking_testdfsdfsdf/entry/lisa/schedule')
        .expectStatus(400)
        .toss();
});
