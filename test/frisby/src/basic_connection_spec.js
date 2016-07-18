describe('HTTP Method Test Suite', function () {
    'use strict';
    var frisby = require('frisby'),
        API = process.env.API_ADDR;

    frisby.create('GET Method')
        .get(API)
        .expectStatus(200)
        .expectHeaderContains('content-type', 'text/html')
        .expectBodyContains('daoserver')
        .toss();
});
