describe("Basic visit", function () {
    "use strict";
    var frisby = require("frisby");

    frisby.create("Homepage")
        .get(process.env.API_ADDR)
        .expectStatus(200)
        .expectHeaderContains("content-type", "text/html")
        .expectBodyContains("Tournament Organiser")
        .toss();
});
