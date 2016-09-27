describe("See the schedule for an entry in a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        injector = require("./data_injector"),
        API = process.env.API_ADDR + "tournament/schedule_test/";

    injector.createUser("permission_test_player");
    injector.createTournament("permission_test", "2095-07-06");
    injector.enterTournament("permission_test", "permission_test_player");

    frisby.create("See lisa schedule")
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

    injector.postRounds("schedule_test", 4);
    frisby.create("See homer schedule")
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
            {
                "game_id": Number,
                "table": 3,
                "round": 3,
                "opponent": "BYE"
            },
            {
                "game_id": Number,
                "table": 3,
                "round": 4,
                "opponent": "schedule_test_player_4"
            }
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
