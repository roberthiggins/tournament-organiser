var frisby = require("frisby"),
    utils = require("./utils"),
    API = process.env.API_ADDR + "tournament/mission_test/missions";

describe("No auth", function () {
    "use strict";
    frisby.create("no auth for missions page")
        .get(API)
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("No auth for missions page content")
        .get(API + "/content")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("No auth for posting missions")
        .post(API, {}, {json: true, inspectOnFailure: true})
        .expectStatus(302)
        .toss();
});

describe("Bad path", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Non-existent tournament content")
            .get(process.env.API_ADDR + "tournament/foo/missions/content")
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
        });
});

describe("Get missions", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Get a list of missions")
            .get(API + "/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({missions: [
                "Mission the First",
                "Mission the Second",
                "Mission the Third"]})
            .toss();
        });
});

describe("Bad submissions", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("POST a single mission only")
            .post(API, {missions: ["mission_1"]},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament mission_test has 3 rounds. " +
                "You submitted missions [\"mission_1\"]"})
            .after(function() {
                frisby.create("check that missions is NOT updated")
                    .get(API + "/content")
                    .addHeader("cookie", cookie)
                    .expectStatus(200)
                    .expectJSON({missions: [
                        "Mission the First",
                        "Mission the Second",
                        "Mission the Third"]})
                    .toss();
                })
            .toss();
        });
});

describe("POST missions", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("POST a correct mission list")
            .post(process.env.API_ADDR + "tournament/mission_test_2/missions",
                {missions: ["m_1", "m_2", "m_3"]},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({message: "Tournament mission_test_2 updated"})
            .after(function() {
                frisby.create("check that missions is updated")
                    .get(process.env.API_ADDR +
                        "tournament/mission_test_2/missions/content")
                    .addHeader("cookie", cookie)
                    .expectStatus(200)
                    .expectJSON({missions: ["m_1", "m_2", "m_3"]})
                    .toss();
                })
            .toss();
        });
});
