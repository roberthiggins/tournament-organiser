var frisby = require("frisby"),
    tournament = "enter_score_test",
    p1 = tournament + "_p_1",
    p2 = tournament + "_p_2",
    API = process.env.API_ADDR + "tournament/enter_score_test/entry/";

var postScore = function(api, player, user, msg, key, score, code, resp){
    var scoreKey = key ? key : "enter_score_test_per_tourn_1";
    frisby.create("POST tournament score: " + msg)
        .post(api + player + "/entertournamentscore",
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
        .post(API + p1 + "/entertournamentscore",
            {
                key: "enter_score_test_1",
                value: 5
            },
            {json: true})
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();

    var post = postScore.bind(this, API, p1);
    post("charlie_murphy", "Random user", null, 5, 403, "Permission denied");
    post(p2, "Different entry", null, 5, 403, "Permission denied");
    post("superuser", "Superuser", "enter_score_test_per_tourn_su", 5, 200,
        "Score entered for " + p1 + ": 5");
    post("enter_score_test_to", "TO", "enter_score_test_per_tourn_to", 5, 200,
        "Score entered for " + p1 + ": 5");


    post = postScore.bind(this, API, p1, p1);
    post("Player", null, 5, 200, "Score entered for " + p1 + ": 5");

    post("Player enters a score twice", null, 4, 400,
        "4 not entered. Score is already set");

    post("Score too low", null, 0, 400, "Invalid score: 0");
    post("Score too high", null, 16, 400, "Invalid score: 16");
    post("Fake category", "non_ex", 5, 400, "Unknown category: non_ex");
    post("Per game category", "enter_score_test_per_game_1", 5, 400,
        "enter_score_test_per_game_1 should be entered per-tournament");
});
