describe('Getting tournament information', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('Details for existing tournament')
        .get(URL + '/tournament/northcon_2095')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSON({
            date: '2095-06-01',
            name: 'northcon_2095',
            rounds: 0
        })
        .toss();

    frisby.create('Non-existent tournament')
        .get(URL + '/tournament/not_a_tournament')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Tournament not_a_tournament not found in database')
        .toss();
});
