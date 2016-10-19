var frisby = require("frisby"),
    injector = require("./data_injector");

var setup = function setup(tourn, players) {
    var categories = [
        [tourn + "_per_tourn_1", 1, true, 4, 15],
        [tourn + "_per_tourn_su", 1, true, 1, 5],
        [tourn + "_per_tourn_to", 1, true, 1, 5],
        [tourn + "_per_game_1", 1, false, 4, 15, true],
        [tourn + "_per_game_2", 1, false, 1, 5, true],
        [tourn + "_per_game_opp", 1, false, 1, 5, false, true],
        [tourn + "_per_game_su", 1, false, 1, 5, true],
        [tourn + "_per_game_to", 1, false, 1, 5, true]
    ];
    injector.createTournament(tourn, "2095-10-10", 1, null, categories, players);
    };

injector.createUser("charlie_murphy");

describe("Enter score for single game for an entry", function () {
    "use strict";

    var tourn = "enter_score_test_1",
        p1 = tourn + "_p_1",
        p2 = tourn + "_p_2",
        API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";
    setup(tourn, [p1, p2]);

    frisby.create("get game_id of next game for " + p1)
        .get(API + p1 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id,
                post = injector.enterScore.bind(this, false, tourn, p1);

            post(null, "No auth enters a score", null, 5, 401,
                "Could not verify your access level", gameId);
            post("charlie_murphy", "Non-playing user", null, 5, 403,
                "Permission denied", gameId);
            post("superuser", "Superuser", tourn + "_per_game_su", 5,
                200, "Score entered for " + p1 + ": 5", gameId);
            post(tourn + "_to", "TO", tourn + "_per_game_to",
                5, 200, "Score entered for " + p1 + ": 5", gameId);

            post = injector.enterScore.bind(this, false, tourn, p1, p1);

            post("Player", null, 5, 200, "Score entered for " + p1 + ": 5",
                gameId);

            post("Player enters a score twice", null, 4, 400,
                "4 not entered. Score is already set", gameId);

            post("Score too low", null, 0, 400, "Invalid score: 0", gameId);
            post("Score too high", null, 16, 400, "Invalid score: 16", gameId);
            post("Fake category", "non_existent", 5, 400,
                "Unknown category: non_existent", gameId);
            post("Per tournament category", tourn + "_per_tourn_1", 5, 400,
                "Cannot enter a per-tournament score (" + tourn +
                "_per_tourn_1) for a game (id: " + gameId + ")", gameId);
        })
        .toss();
});

describe("Oppostion scores", function() {
    "use strict";

    var tourn = "enter_score_test_2",
        p1 = tourn + "_p_1",
        p2 = tourn + "_p_2",
        API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";
    setup(tourn, [p1, p2]);

    frisby.create("get game_id of next game for " + p2)
        .get(API + p1 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id,
                post = injector.enterScore.bind(this, false, tourn, p1, p1);
            post("P1 enters opp score", tourn + "_per_game_opp", 4, 200,
                "Score entered for " + p2 + ": 4", gameId); // NB P2

            post("P1 enters opp score again", tourn + "_per_game_opp", 4, 400,
                "4 not entered. Score is already set", gameId);
        })
        .toss();
});

describe("Zero Sum scores", function () {
    "use strict";

    var tourn = "enter_score_test_3",
        p1 = tourn + "_p_1",
        p2 = tourn + "_p_2",
        API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";
    setup(tourn, [p1, p2]);

    frisby.create("get game_id of next game for " + p2)
        .get(API + p2 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id,
                cat = tourn + "_per_game_2",
                post = injector.enterScore.bind(this, false, tourn, p1);

            post(p1, "P1 enters zero_sum score", cat, 4, 200,
                "Score entered for " + p1 + ": 4", gameId);


            post = injector.enterScore.bind(this, false, tourn, p2, p2);
            post("P2 enters zero_sum score that is too high", cat, 2, 400,
                "Invalid score: 2", gameId);
            post("P2 enters zero_sum score that is acceptable",cat, 1, 200,
                "Score entered for " + p2 + ": 1", gameId);
        })
        .toss();
});
