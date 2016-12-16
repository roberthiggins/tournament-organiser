var frisby = require("frisby"),
    utils = require("./utils"),
    rounds_test_api = process.env.API_ADDR + "tournament/rounds_test/rounds";

describe("No auth", function () {
    "use strict";
    frisby.create("No auth for setting rounds")
        .post(rounds_test_api, {rounds: 1},
            {json: true, inspectOnFailure: true})
        .expectStatus(302)
        .toss();

    frisby.create("Get page")
        .get(rounds_test_api, {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("Get page content")
        .get(rounds_test_api + "/content", {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();
});

describe("Bad tournament", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/foo/rounds";

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Set rounds for non-existent tournament")
            .get(API, {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectBodyContains("tournamentRounds.js")
            .toss();
        });

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Content for non-existent tournament")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
        });

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Set rounds for non-existent tournament")
            .post(API, {}, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
        });
});

describe("Set rounds for a tournament", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Get basic page")
            .get(rounds_test_api, {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectBodyContains("tournamentRounds.js")
            .toss();
        });

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Set rounds tournament")
            .post(rounds_test_api, {rounds: 6},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({message: "Tournament rounds_test updated"})
            .after(function() {
                utils.asUser("superman", "password", function(cookie) {
                    frisby.create("See that rounds are now set")
                        .get(rounds_test_api + "/content",
                            {inspectOnFailure: true})
                        .addHeader("cookie", cookie)
                        .expectStatus(200)
                        .expectJSON({rounds: 6})
                        .toss();
                        });
                })
            .toss();
        });
});

describe("Set illegal rounds for a tournament", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("character")
            .post(rounds_test_api, {rounds: "a"},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Natural number required"})
            .toss();
        });
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("negative")
            .post(rounds_test_api, {rounds: -1},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Natural number required"})
            .toss();
        });
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("decimal")
            .post(rounds_test_api, {rounds: 1.5},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Natural number required"})
            .toss();
        });
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("empty")
            .post(rounds_test_api, {rounds: ""},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Natural number required"})
            .toss();
        });
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("null")
            .post(rounds_test_api, {}, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Natural number required"})
            .toss();
        });
});
