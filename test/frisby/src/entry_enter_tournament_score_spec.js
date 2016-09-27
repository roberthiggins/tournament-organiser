var frisby = require("frisby"),
    tournament = "enter_score_test",
    p1 = tournament + "_p_1",
    p2 = tournament + "_p_2",
    API = process.env.API_ADDR + "tournament/enter_score_test/entry/";

var postScore = function(msg, user, key, score, code, resp){
    var scoreKey = key ? key : "enter_score_test_category_per_tournament_1";
    frisby.create("POST tournament score: " + msg)
        .post(API + p1 + "/entertournamentscore",
            {
                key: scoreKey,
                value: score
            },
            {json: true, inspectOnFailure: true})
        .addHeader("Authorization", "Basic " +
            new Buffer(user + ":password").toString("base64"))
        .expectStatus(code)
        .expectBodyContains(resp)
        .toss();
};

describe("Enter a tournament score for an entry", function () {
    "use strict";

    frisby.create("No auth enters a score")
        .post(API + "enter_score_test_p_1/entertournamentscore",
            {
                key: "enter_score_test_category_1",
                value: 5
            },
            {json: true})
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();

    postScore("Non-playing user", "charlie_murphy", null, 5,
        403, "Permission denied");
    postScore("Different entry", p2, null, 5, 403, "Permission denied");
    postScore("Superuser", "superuser",
        "enter_score_test_category_per_tournament_su", 5, 200,
        "Score entered for enter_score_test_p_1: 5");
    postScore("TO", "enter_score_test_to",
        "enter_score_test_category_per_tournament_to", 5, 200,
        "Score entered for enter_score_test_p_1: 5");
    postScore("Player", p1, null, 5, 200,
        "Score entered for enter_score_test_p_1: 5");

    postScore("Player enters a score twice", p1, null, 4, 400,
        "4 not entered. Score is already set");

    postScore("Score too low", p1, null, 0, 400, "Invalid score: 0");
    postScore("Score too high", p1, null, 16, 400, "Invalid score: 16");
    postScore("Fake category", p1, "enter_score_test_category_non_existent",
        5, 400, "Unknown category: enter_score_test_category_non_existent");
    postScore("Per game category", p1, "enter_score_test_category_per_game_1",
        5, 400, "enter_score_test_category_per_game_1 should be " +
        "entered per-tournament");
});
