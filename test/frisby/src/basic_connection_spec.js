describe('HTTP Method Test Suite', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('GET Method')
        .get(URL + '/')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('daoserver')
        .toss();
});
