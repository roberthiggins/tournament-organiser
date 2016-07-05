describe('Get a list of entries from a tournament', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR']

    frisby.create('Details for existing tournament')
        .get(API + 'tournament/ranking_test/entry/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes('*', String)
        .expectJSON([
            'homer',
            'marge',
            'lisa',
            'bart',
            'maggie'
        ])
        .toss();

    frisby.create('Tournament with no entries')
        .get(API + 'tournament/permission_test/entry/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();

    frisby.create('Tournament that does not exist')
        .get(API + 'tournament/kdjflskdjflkdjflkdjf/entry/')
        .expectStatus(400)
        .toss();
});
