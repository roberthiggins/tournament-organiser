var frisby = require("frisby"),
    injector = require("./data_injector"),
    tourn = "enter_score_test",
    p1 = tourn + "_p_1",
    p2 = tourn + "_p_2",
    API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";

var postScore = function(api, player, msg, gameId, user, scoreKey, score, code,
        resp){
    var key = scoreKey ? scoreKey : "enter_score_test_category_per_game_1";
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

(function setup() {
    injector.createUser("charlie_murphy");

    var categories = [
        [tourn + "_category_per_tournament_1", 1, true, 4, 15],
        [tourn + "_category_per_tournament_su", 1, true, 1, 5],
        [tourn + "_category_per_tournament_to", 1, true, 1, 5],
        [tourn + "_category_per_game_1", 1, false, 4, 15, true],
        [tourn + "_category_per_game_2", 1, false, 1, 5, true],
        [tourn + "_category_per_game_opp", 1, false, 1, 5, false, true],
        [tourn + "_category_per_game_su", 1, false, 1, 5, true],
        [tourn + "_category_per_game_to", 1, false, 1, 5, true]
    ];
    injector.createTournament(tourn, "2095-10-10", 1, null, categories);
    injector.createUser(p1);
    injector.createUser(p2);
    injector.enterTournament(tourn, p1);
    injector.enterTournament(tourn, p2);
})();

describe("Enter score for single game for an entry", function () {
    "use strict";

    frisby.create("get game_id of next game for enter_score_test_p_1")
        .get(API + p1 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id;

            frisby.create("No auth enters a score")
                .post(API + p1 + "/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_1",
                        value: 5
                    },
                    {json: true, inspectOnFailure: true})
                .expectStatus(401)
                .expectBodyContains("Could not verify your access level")
                .toss();

            var post = postScore.bind(this, API, p1);

            post("Non-playing user", gameId, "charlie_murphy", null, 5,
                403, "Permission denied");
            post("Different entry", gameId, p2, null, 5, 403,
                "Permission denied");
            post("Superuser", gameId, "superuser",
                "enter_score_test_category_per_game_su", 5, 200,
                "Score entered for enter_score_test_p_1: 5");
            post("TO", gameId, "enter_score_test_to",
                "enter_score_test_category_per_game_to", 5, 200,
                "Score entered for enter_score_test_p_1: 5");
            post("Player", gameId, p1, null, 5, 200,
                "Score entered for enter_score_test_p_1: 5");

            post("Player enters a score twice",gameId,  p1, null, 4, 400,
                "4 not entered. Score is already set");

            post("Score too low", gameId, p1, null, 0, 400,
                "Invalid score: 0");
            post("Score too high", gameId, p1, null, 16, 400,
                "Invalid score: 16");
            post("Fake category", gameId, p1,
                "enter_score_test_category_non_existent", 5, 400,
                "Unknown category: enter_score_test_category_non_existent");
            post("Per tournament category", gameId, p1,
                "enter_score_test_category_per_tournament_1", 5, 400,
                "Cannot enter a per-tournament score " +
                "(enter_score_test_category_per_tournament_1) for a game " +
                "(id: " + gameId + ")");
        })
        .toss();
});

describe("Oppostion scores", function() {
    "use strict";
    frisby.create("get game_id of next game for enter_score_test_p_2")
        .get(API + p1 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id,
                post = postScore.bind(this, API, p1);
            post("P1 enters opp score", gameId, p1,
                "enter_score_test_category_per_game_opp", 4, 200,
                "Score entered for enter_score_test_p_2: 4"); // NB P2

            post("P1 enters opp score again", gameId, p1,
                "enter_score_test_category_per_game_opp", 4, 400,
                "4 not entered. Score is already set");
        })
        .toss();
});

describe("Zero Sum scores", function () {
    "use strict";

    frisby.create("get game_id of next game for enter_score_test_p_2")
        .get(API + p2 + "/nextgame")
        .expectStatus(200)
        .afterJSON(function (body) {
            var gameId = body.game_id,
                auth = injector.auth("enter_score_test_p_2"),
                post = postScore.bind(this, API, p1);
            post("P1 enters zero_sum score", gameId, p1,
                "enter_score_test_category_per_game_2", 4, 200,
                "Score entered for enter_score_test_p_1: 4");

            frisby.create("player 2 enters a zero_sum score that is too high")
                .post(API + p2 + "/entergamescore",
                    {
                        game_id: gameId,
                        key: "enter_score_test_category_per_game_2",
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
                        key: "enter_score_test_category_per_game_2",
                        value: 1
                    },
                    {json: true})
                .addHeader("Authorization", auth)
                .expectStatus(200)
                .expectBodyContains(
                    "Score entered for enter_score_test_p_2: 1")
                .toss();

        })
        .toss();
});
