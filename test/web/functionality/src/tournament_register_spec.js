var frisby = require("frisby"),
    utils = require("./utils"),
    register_test_api = process.env.API_ADDR + "tournament/register_test_1";

describe("No auth", function () {
    "use strict";
    frisby.create("No auth for applying")
        .post(process.env.API_ADDR + "tournament/mission_test",
            {json: true, inspectOnFailure: true})
        .expectStatus(302)
        .toss();
});

describe("Bad tournament", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/foo";

    frisby.create("Info about non-existent tournament")
        .get(API, {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("tournamentInfo.js")
        .toss();

    frisby.create("Content for non-existent tournament")
        .get(API + "/content", {inspectOnFailure: true})
        .expectStatus(400)
        .expectJSON({error: "Tournament foo not found in database"})
        .toss();

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Apply to non-existent tournament")
            .post(API, {}, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
        });
});

describe("Register for tournament", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Apply to a tournament")
            .post(register_test_api, {}, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({message: "Application Submitted"})
            .after(function() {
                utils.asUser("superman", "password", function(cookie) {
                    frisby.create("Check that entry is now confirmed")
                        .get(register_test_api + "/entries/content",
                            {inspectOnFailure: true})
                        .addHeader("cookie", cookie)
                        .expectStatus(200)
                        .expectJSON({entries: ["superman"]})
                        .toss();
                        });
                })
            .toss();
        });
});
