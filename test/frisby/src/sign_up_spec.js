describe('Signing up and seeing user details', function() {
    var frisby = require('frisby');
    var URL = 'http://' + process.env['DAOSERVER_PORT_5000_TCP_ADDR'] + ':'
        + process.env['DAOSERVER_PORT_5000_TCP_PORT'];

    frisby.create('See user details')
        .get(URL + '/user/charlie_murphy')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({charlie_murphy: String})
        .expectJSON({charlie_murphy: 'charlie_murphy@darkness.com'})
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(URL + '/user/')
        .expectStatus(404)
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(URL + '/user/jim_bob_noname')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Cannot find user jim_bob_noname')
        .toss();
});
