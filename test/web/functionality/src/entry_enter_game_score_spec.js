var frisby = require("frisby"),
    utils = require("./utils");

describe("Check auth for page", function () {
    "use strict";
    frisby.create("Visit page with no auth")
        .get(process.env.API_ADDR + "tournament/enter_score_test/entry/enter_score_test_player_5/entergamescore")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("Content with no auth")
        .get(process.env.API_ADDR + "tournament/enter_score_test/entry/enter_score_test_player_5/entergamescore/content")
        .expectStatus(200)
        .expectJSON({
            error: "Could not verify your access level for that URL.\nYou have to login with proper credentials"
            })
        .toss();
});

describe("Bad targets", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/enter_score_test/entry/";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("No game scheduled")
            .get(API + "enter_score_test_player_1/entergamescore/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                error: "Next game not scheduled. Check with the TO."
                })
            .toss();
        });

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("non-user")
            .get(API + "enter_score_test_p_non/entergamescore/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                error: "Unknown player: enter_score_test_p_non"
                })
            .toss();
        });
});

describe("Enter some scores", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/enter_score_test/" +
        "entry/enter_score_test_player_5/entergamescore",
        badValues = function(user, pass, postData, name, msg) {

            utils.asUser(user, pass, function(cookie) {
                frisby.create("get game_id")
                    .get(API + "/content")
                    .addHeader("cookie", cookie)
                    .afterJSON(function(json) {
                        var scoreInfo = postData;
                        scoreInfo.gameId = json.game_id;

                        frisby.create(name)
                            .post(API, scoreInfo)
                            .addHeader("cookie", cookie)
                            .expectStatus(400)
                            .expectJSON({error: msg})
                            .toss();
                        })
                    .toss();
                });
            };

    badValues("enter_score_test_player_2", "password",
        {key: "Fair Play", value: 5},
        "Other user",
        "Permission denied for enter_score_test_player_2 to perform enter_score on tournament enter_score_test");

    badValues("enter_score_test_player_5", "password",
        {key: "Fair Play", value: 0},
        "Invalid score",
        "Invalid score: 0");

    utils.asUser("enter_score_test_player_5", "password", function(cookie) {
        frisby.create("get game_id")
            .get(API + "/content")
            .addHeader("cookie", cookie)
            .afterJSON(function(json) {
                var scoreInfo = {
                        gameId: json.game_id,
                        key: "Fair Play",
                        value: 5};

                frisby.create("Enter good score")
                    .post(API, scoreInfo)
                    .addHeader("cookie", cookie)
                    .expectStatus(200)
                    .expectJSON({
                        message: "Score entered for enter_score_test_player_5: 5"
                        })
                    .toss();
                })
            .toss();
        });

    badValues("enter_score_test_player_5", "password",
        {key: "Fair Play", value: 5},
        "Enter score twice",
        "5 not entered. Score is already set");

});
