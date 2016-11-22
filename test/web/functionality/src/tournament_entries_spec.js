var frisby = require("frisby"),
    utils = require("./utils"),
    API = process.env.API_ADDR + "tournament/";

describe("Auth", function () {
    "use strict";
    var tourn = "entries_test";
    frisby.create("basic page - no auth")
        .get(API + tourn + "/entries", {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create(tourn + " content - no auth")
        .get(API + tourn + "/entries/content", {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();
});

describe("Bad tournament", function () {
    "use strict";
    var tourn = "foo";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("basic page for " + tourn)
            .get(API + tourn + "/entries", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectBodyContains("entry.js")
            .toss();

        frisby.create(tourn + " content")
            .get(API + tourn + "/entries/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo doesn't exist"})
            .toss();
    });
});

describe("Get entries page", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {
        var tourn = "entries_test";
        frisby.create(tourn + " content")
            .get(API + tourn + "/entries/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                entries: ["entries_test_p_1"],
                tournament: tourn
                })
            .toss();

        frisby.create("No players entered")
            .get(API + "empty_tournament/entries/content",
                {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                entries: [],
                tournament: "empty_tournament"
                })
            .toss();
    });
});
