describe("Enter score for single game for an entry", function () {
    "use strict";
    var frisby = require("frisby"),
        injector = require("./data_injector"),
        API = process.env.API_ADDR + "tournament/enter_score_test/entry/";

    // Some setup
    injector.postRounds("enter_score_test", 1);
    frisby.create("get game_id of next game for enter_score_test_p_1")
        .get(API + "enter_score_test_p_1/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id;

            frisby.create("No auth enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_1",
                        value: 5
                    },
                    {json: true})
                .expectStatus(401)
                .expectBodyContains("Could not verify your access level")
                .toss();

            frisby.create("Non-playing user enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_1",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " +
                    new Buffer("charlie_murphy:password").toString("base64"))
                .expectStatus(403)
                .expectBodyContains("Permission denied")
                .toss();

            frisby.create("Different entry enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_1",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_2:password").toString("base64"))
                .expectStatus(403)
                .expectBodyContains("Permission denied")
                .toss();

            frisby.create("superuser enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_su",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " +
                    new Buffer("superuser:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_1: 5")
                .toss();


            frisby.create("to enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_to",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_to:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_1: 5")
                .toss();

            frisby.create("player enters a score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_1",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_1" +
                    ": 5")
                .toss();


            frisby.create("player enters a score twice: first score")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_2",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_1: 5")
                .toss();
            frisby.create("player enters a score twice: again")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_2",
                        value: 4
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("4 not entered. Score is already set")
                .toss();


            frisby.create("score too low")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_3",
                        value: 0
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("Invalid score: 0")
                .toss();


            frisby.create("score too high")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_3",
                        value: 6
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("Invalid score: 6")
                .toss();

            frisby.create("Non-existent category")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_non_existent",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("Unknown category: " +
                    "enter_score_test_category_non_existent")
                .toss();

            frisby.create("Per tournament category")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_1",
                        value: 5
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("Cannot enter a per-tournament score " +
                    "(enter_score_test_category_1) for a game (game_id: " +
                    gameId + ")")
                .toss();

        })
        .toss();

    frisby.create("get game_id of next game for enter_score_test_p_2")
        .get(API + "enter_score_test_p_2/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id;

            frisby.create("player enters a zero_sum score that is too high")
                .post(API + "enter_score_test_p_1/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_4",
                        value: 4
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_1:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_1" +
                    ": 4")
                .toss();

            frisby.create("player enters a zero_sum score that is too high")
                .post(API + "enter_score_test_p_2/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_4",
                        value: 2
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_2:password").toString("base64"))
                .expectStatus(400)
                .expectBodyContains("Invalid score: 2")
                .toss();

            frisby.create("player enters a zero_sum score acceptably")
                .post(API + "enter_score_test_p_2/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_4",
                        value: 1
                    },
                    {json: true})
                .addHeader("Authorization", "Basic " + new Buffer(
                    "enter_score_test_p_2:password").toString("base64"))
                .expectStatus(200)
                .expectBodyContains("Score entered for enter_score_test_p_2" +
                    ": 1")
                .toss();

        })
        .toss();
});
