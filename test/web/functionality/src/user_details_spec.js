var frisby = require("frisby"),
    utils = require("./utils"),
    API = process.env.API_ADDR + "user/ranking_test_player_1";

describe("Auth", function () {
    "use strict";

    frisby.create("No auth for to see page at all")
        .get(API, {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("No auth for random to see details")
        .get(API + "/content", {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("superuser can see details")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                user: {
                    username: "ranking_test_player_1",
                    first_name: "ranking_test",
                    last_name: "P1",
                    email: "ranking_test_player_1@bar.com"
                    }
                })
            .toss();
        });

    utils.asUser("ranking_test_to", "password", function(cookie) {
        frisby.create("other users cannot see details")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Permission denied for ranking_test_to"})
            .toss();
        });
});

describe("Bad user", function () {
    "use strict";
    var API = process.env.API_ADDR + "user/foo";

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Details for non-existent user")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Cannot find user foo"})
            .toss();
        });
});

describe("See user details", function () {
    "use strict";

    utils.asUser("ranking_test_player_1", "password", function(cookie) {
        frisby.create("superuser can see details")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                user: {
                    username: "ranking_test_player_1",
                    first_name: "ranking_test",
                    last_name: "P1",
                    email: "ranking_test_player_1@bar.com"
                    }
                })
            .toss();
        });
});
