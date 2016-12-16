var frisby = require("frisby"),
    API = process.env.API_ADDR + "tournament/";

describe("Get draw page", function () {
    "use strict";
    frisby.create("basic page")
        .get(API + "foo/round/1/draw", {inspectOnFailure: true})
        .expectStatus(200)
        .expectBodyContains("tournamentDraw.js")
        .toss();

    var tourn = "ranking_test";
    frisby.create(tourn + " content")
        .get(API + tourn + "/round/1/draw/content",
            {inspectOnFailure: true})
        .expectStatus(200)
        .expectJSON({
            draw: [
                {   table_number: 1,
                    entrants: [tourn + "_player_3", "BYE"] },
                {   table_number: 2,
                    entrants: [tourn + "_player_1", tourn + "_player_5"]},
                {   table_number: 3,
                    entrants: [tourn + "_player_2", tourn + "_player_4"]}
                ],
            mission: "Kill",
            tournament: tourn,
            round: "1"
            })
        .toss();

    frisby.create("No draw available")
        .get(API + "mission_test/round/1/draw/content",
            {inspectOnFailure: true})
        .expectStatus(200)
        .expectJSON({
            draw: [],
            mission: "Mission the First",
            tournament: "mission_test",
            round: "1"
            })
        .toss();
});

describe("Get the draw bad values", function () {
    "use strict";
    frisby.create("bad tournament")
        .get(API + "foo/round/1/draw/content", {inspectOnFailure: true})
        .expectStatus(400)
        .expectJSON({error: "Tournament foo not found in database"})
        .toss();

    frisby.create("Round that does not exist")
        .get(API + "ranking_test/round/3/draw/content",
            {inspectOnFailure: true})
        .expectStatus(400)
        .expectJSON({error: "Tournament ranking_test does not have a round 3"})
        .toss();
});
