describe('Get a list of entries from a tournament', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('Details for existing tournament')
        .get(URL + '/tournament/ranking_test/entry/')
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
        .get(URL + '/tournament/permission_test/entry/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON([])
        .toss();

    frisby.create('Tournament that does not exist')
        .get(URL + '/tournament/kdjflskdjflkdjflkdjf/entry/')
        .expectStatus(404)
        .toss();
});
