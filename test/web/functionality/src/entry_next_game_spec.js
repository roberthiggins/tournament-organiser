var frisby = require("frisby"),
    utils = require("./utils");

describe("Content with auth", function () {
    "use strict";
    var API = process.env.API_ADDR +
            "tournament/next_game_test/entry/next_game_test_player_5/nextgame";
    frisby.create("Next game page")
        .get(API)
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("Next game page content")
        .get(API + "/content")
        .expectStatus(200)
        .expectJSON({error: "Could not verify your access level for that URL.\nYou have to login with proper credentials"})
        .toss();
});

describe("Bad targets", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
         frisby.create("non-existent tournament")
            .addHeader("cookie", cookie)
            .get(process.env.API_ADDR +
                "tournament/foo/entry/next_game_test_player_5/nextgame/content")
            .expectStatus(200)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
       });

    utils.asUser("superman", "password", function(cookie) {
         frisby.create("non-existent entry")
            .addHeader("cookie", cookie)
            .get(process.env.API_ADDR +
                "tournament/next_game_test/entry/ranking_test_player_1" +
                "/nextgame/content")
            .expectStatus(200)
            .expectJSON({
                error: "Entry for ranking_test_player_1 in tournament " +
                    "next_game_test not found"})
            .toss();
       });

    utils.asUser("superman", "password", function(cookie) {
         frisby.create("non-existent user")
            .addHeader("cookie", cookie)
            .get(process.env.API_ADDR +
                "tournament/next_game_test/entry/noone/nextgame/content")
            .expectStatus(200)
            .expectJSON({error: "Unknown player: noone"})
            .toss();
       });

    var player = "enter_score_test_player_3";
    utils.asUser(player, "password", function(cookie) {
         frisby.create("entry who has played all games")
            .addHeader("cookie", cookie)
            .get(process.env.API_ADDR +
                "tournament/enter_score_test/entry/" + player +
                "/nextgame/content", {inspectOnFailure: true})
            .expectStatus(200)
            .expectJSON({
                error: "Next game not scheduled. Check with the TO.",
                nextgame: null
            })
            .toss();
       });
});

describe ("Happy path", function() {

    var player = "enter_score_test_player_5";
    utils.asUser(player, "password", function(cookie) {
         frisby.create("get round two score entry page")
            .addHeader("cookie", cookie)
            .get(process.env.API_ADDR +
                "tournament/enter_score_test/entry/" + player +
                "/nextgame/content", {inspectOnFailure: true})
            .expectStatus(200)
            .expectJSON({
                message: 'Next Game Info for enter_score_test_player_5',
                nextgame: {
                    game_id: Number,
                    table: 2,
                    mission: "TBA",
                    round: 2,
                    opponent: "enter_score_test_player_4"
                }
            })
            .toss();
       });
});
