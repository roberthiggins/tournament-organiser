describe('Signing up and seeing user details', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('See user details')
        .get(API + 'user/charlie_murphy')
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(200)
        .expectHeaderContains('content-type', 'application/json')
        .expectJSONTypes({charlie_murphy: String})
        .expectJSON({charlie_murphy: 'charlie_murphy@bar.com'})
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(API + 'user/')
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(404)
        .toss();

    frisby.create('Look for a user who doesn\'t exist')
        .get(API + 'user/jim_bob_noname')
        .addHeader('Authorization', "Basic " +
            new Buffer('superuser:password').toString("base64"))
        .expectStatus(400)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('Cannot find user jim_bob_noname')
        .toss();

    frisby.create('See user details with no auth')
        .get(API + 'user/charlie_murphy')
        .expectStatus(401)
        .toss();

    frisby.create('See user details with bad auth')
        .get(API + 'user/charlie_murphy')
        .addHeader('Authorization', "Basic " +
            new Buffer('noone:password').toString("base64"))
        .expectStatus(401)
        .toss();
});
