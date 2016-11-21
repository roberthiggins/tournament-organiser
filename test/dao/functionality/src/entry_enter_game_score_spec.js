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
    injector.createTournament(tourn, "2095-10-10", 1, null, categories);
    (players || []).forEach(function(player) {
        injector.createUser(player);
        injector.enterTournament(tourn, player);
        });
    },
    postScore = function(tourn, api, player, gameId, msg, user, scoreKey,
        score, code, resp){
        var key = scoreKey ? scoreKey : tourn + "_per_game_1";
        frisby.create("POST score: " + msg)
            .post(api + player + "/entergamescore",
                {
                    game_id: gameId,
                    key: key,
                    value: score
                },
                {json: true, inspectOnFailure: true})
            .addHeader("Authorization", injector.auth(user))
            .expectStatus(code)
            .expectBodyContains(resp)
            .toss();
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
            var gameId = body.game_id;

            frisby.create("No auth enters a score")
                .post(API + p1 + "/entergamescore",
                    {
                        game_id: gameId,
                        key: tourn + "_per_game_1",
                        value: 5
                    },
                    {json: true, inspectOnFailure: true})
                .expectStatus(401)
                .expectBodyContains("Could not verify your access level")
                .toss();

            var post = postScore.bind(this, tourn, API, p1, gameId);

            post("Non-playing user", "charlie_murphy", null, 5, 403,
                "Permission denied");
            post("Superuser", "superuser", tourn + "_per_game_su", 5,
                200, "Score entered for " + p1 + ": 5");
            post("TO", tourn + "_to", tourn + "_per_game_to",
                5, 200, "Score entered for " + p1 + ": 5");
            post("Player", p1, null, 5, 200, "Score entered for " + p1 + ": 5");

            post("Player enters a score twice", p1, null, 4, 400,
                "4 not entered. Score is already set");

            post("Score too low", p1, null, 0, 400, "Invalid score: 0");
            post("Score too high", p1, null, 16, 400, "Invalid score: 16");
            post("Fake category", p1, "non_existent", 5, 400,
                "Unknown category: non_existent");
            post("Per tournament category", p1, tourn + "_per_tourn_1",
                5, 400, "Cannot enter a per-tournament score (" + tourn +
                "_per_tourn_1) for a game (id: " + gameId + ")");
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
                post = postScore.bind(this, tourn, API, p1, gameId);
            post("P1 enters opp score", p1,
                tourn + "_per_game_opp", 4, 200,
                "Score entered for " + p2 + ": 4"); // NB P2

            post("P1 enters opp score again", p1,
                tourn + "_per_game_opp", 4, 400,
                "4 not entered. Score is already set");
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
                auth = injector.auth(p2),
                post = postScore.bind(this, tourn, API, p1, gameId);
            post("P1 enters zero_sum score", p1, tourn + "_per_game_2",
                4, 200, "Score entered for " + p1 + ": 4");

            frisby.create("player 2 enters a zero_sum score that is too high")
                .post(API + p2 + "/entergamescore",
                    {
                        game_id: gameId,
                        key: tourn + "_per_game_2",
                        value: 2
                    },
                    {json: true})
                .addHeader("Authorization", auth)
                .expectStatus(400)
                .expectBodyContains("Invalid score: 2")
                .toss();

            frisby.create("player enters a zero_sum score acceptably")
                .post(API + p2 + "/entergamescore",
                    {
                        game_id: gameId,
                        key: tourn + "_per_game_2",
                        value: 1
                    },
                    {json: true})
                .addHeader("Authorization", auth)
                .expectStatus(200)
                .expectBodyContains(
                    "Score entered for " + p2 + ": 1")
                .toss();

        })
        .toss();
});
