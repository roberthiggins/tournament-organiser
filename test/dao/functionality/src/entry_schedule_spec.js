describe("See the schedule for an entry in a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        injector = require("./data_injector"),
        API = process.env.API_ADDR + "tournament/schedule_test/";

    injector.createTournament("permission_test", "2095-07-06", null, null, null,
        ["permission_test_player"]);

    frisby.create("See player_3 schedule")
        .get(API + "entry/schedule_test_player_3/schedule")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes("*", {
            "table" : Number,
            "game_id": Number,
            "round": Number,
            "opponent": String
        })
        .expectJSON([
            {"table": 1, "game_id": Number, "round": 1, "opponent": "BYE"},
            {"table": 3, "game_id": Number, "round": 2, "opponent": "schedule_test_player_1"}
        ])
        .toss();

    frisby.create("See schedule_test_player_1 schedule")
        .get(API + "entry/schedule_test_player_1/schedule")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([
            {
                "game_id": Number,
                "table": 2,
                "round": 1,
                "opponent": "schedule_test_player_5"
            },
            {
                "game_id": Number,
                "table": 3,
                "round": 2,
                "opponent": "schedule_test_player_3"
            },
        ])
        .toss();

    frisby.create("Entry has not played a game")
        .get(process.env.API_ADDR + "tournament/permission_test/entry/permission_test_player/schedule")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([])
        .toss();

    frisby.create("No entry with that username")
        .get(API + "entry/persona_non_grata")
        .expectStatus(400)
        .toss();

    frisby.create("Tournament that does not exist")
        .get(process.env.API_ADDR + "tournament/sdf/entry/p_1/schedule")
        .expectStatus(400)
        .toss();
});
