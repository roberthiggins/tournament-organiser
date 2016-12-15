var frisby = require("frisby"),
    tourn = "enter_score_test_1",
    p1 = tourn + "_p_1",
    p2 = tourn + "_p_2",
    API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";

var postScore = function(api, player, user, msg, cat, score, code, resp) {
    var scoreKey = cat ? cat : tourn + "_per_tourn_1";
    frisby.create("POST tournament score: " + msg)
        .post(api + player + "/score",
            {
                category: scoreKey,
                score: score
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
        .post(API + p1 + "/score",
            {
                category: tourn,
                score: 5
            },
            {json: true})
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();

    var post = postScore.bind(this, API, p1);
    post("charlie_murphy", "Random user", null, 5, 403, "Permission denied");
    post(p2, "Different entry", null, 5, 403, "Permission denied");
    post("superuser", "Superuser", tourn + "_per_tourn_su", 5, 200,
        "Score entered for " + p1 + ": 5");
    post(tourn + "_to", "TO", tourn + "_per_tourn_to", 5, 200,
        "Score entered for " + p1 + ": 5");


    post = postScore.bind(this, API, p1, p1);
    post("Score too low", null, 0, 400, "Invalid score: 0");
    post("Score too high", null, 16, 400, "Invalid score: 16");
    post("Player", null, 5, 200, "Score entered for " + p1 + ": 5");

    post("Player enters a score twice", null, 4, 400,
        "4 not entered. Score is already set");
    post("Fake category", "non_ex", 5, 400, "Unknown category: non_ex");
    post("Per game category", tourn + "_per_game_1", 5, 400,
        tourn + "_per_game_1 should be entered per-tournament");
});
