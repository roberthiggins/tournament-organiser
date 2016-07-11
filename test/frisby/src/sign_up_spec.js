describe('Signing up and seeing user details', function() {
    var frisby = require('frisby');
    var API = process.env['API_ADDR']

    frisby.create('See user details')
        .get(API + 'user/charlie_murphy')
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({charlie_murphy: String})
        .expectJSON({charlie_murphy: 'charlie_murphy@bar.com'})
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(API + 'user/')
        .expectStatus(404)
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(API + 'user/jim_bob_noname')
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Cannot find user jim_bob_noname')
        .toss();
});
