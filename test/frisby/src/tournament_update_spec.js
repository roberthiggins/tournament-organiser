var frisby = require("frisby"),
    injector = require("./data_injector.js"),
    MASTERAPI = process.env.API_ADDR + "tournament/";

describe("Update a tournament", function () {
    "use strict";

    var tournament = "update_test_1",
        API = MASTERAPI + tournament,
        newCategory = injector.jsonCat(null, "cat_t_three", 99, true, 1, 2,
            false, false),
        newMissions = ["one", "two", "three"];

    injector.createTournament(tournament, "2135-12-08");
    injector.setCategories(tournament, [
        ["cat_t_one", 8, true, 4, 12, false, false],
        ["cat_t_two", 13, false, 3, 11, true, true]]);

    frisby.create("update the tournament")
        .post(API, {
            score_categories: [newCategory],
            rounds: 3,
            missions: newMissions
            }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization",
            injector.auth(tournament + "_to", "password"))
        .expectStatus(200)
        .after(function() {
            frisby.create("New information should be present")
                .get(API)
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSON({
                    date: "2135-12-08",
                    name: tournament,
                    rounds: 3
                })
                .toss();

            frisby.create("New categories should be present")
                .get(API + "/score_categories")
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSON([newCategory])
                .toss();

            frisby.create("New missions should be present")
                .get(API + "/missions")
                .expectStatus(200)
                .expectJSONTypes("*", Array)
                .expectJSON(newMissions)
                .toss();

            })
        .toss();
});
