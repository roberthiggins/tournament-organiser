var frisby = require("frisby"),
    injector = require("./data_injector"),
    tourn = "enter_score_test_8",
    player = tourn + "_p_1",
    user = "superuser",
    cat = tourn + "_cat_1",
    API = process.env.API_ADDR + "tournament/" + tourn + "/entry/" + player;

var enterScore = function(tourn, code, msg, postData, resp){
    frisby.create("POST score: " + msg)
        .addHeader("Authorization", injector.auth(user))
        .post(API + "/score", postData, {json: true, inspectOnFailure: true})
        .expectStatus(code)
        .expectBodyContains(resp)
        .toss();
};

describe("Bad score formats should be rejected", function () {
    "use strict";

    injector.createTournament(tourn, "2095-10-10", 1, null,
        [[cat, 1, true, 4, 15]], [player]);
    var post = enterScore.bind(this, tourn, 400),
        noCat = {
            scores: [
                {score: 5}
            ]
        },
        noScore = {
            scores: [
                {category: cat}
            ]
        },
        keysOnly = {
            scores: [
                {
                    score: null,
                    category: null
                }
            ]
        },
        noKeys = {
            scores: [
                {}
            ]
        },
        noScores = {
            scores: []
        },
        nothing = {},
        emptyCat = {
            scores: [
                {
                    score: 5,
                    category: ''
                }
            ]
        };

    post("No cat",     noCat,      "Unknown category: None");
    post("No score",   noScore,    "Invalid score: None");
    post("Keys only",  keysOnly,   "Invalid score: None");
    post("No keys",    noKeys,     "Invalid score: None");
    post("No Scores",  noScores,   "Invalid score: None");
    post("Empty dict", nothing,    "Invalid score: None");

    post("Empty cat",  emptyCat,   "Unknown category: ");
});

describe("Bad score values should be rejected", function () {
    "use strict";

    var tourn = "enter_score_test_7",
        p1 = tourn + "_p_1",
        cat1 = tourn + "_per_tourn_1",
        cat2 = tourn + "_per_tourn_2",
        post = injector.enterScore.bind(this, true, tourn, p1, p1),
        cats = [
            [cat1, 1, true, 4, 15],
            [cat2, 1, true, 1, 5]
        ];
    injector.createTournament(tourn, "2095-10-10", 1, null, cats, [p1]);

    post("Missing score", [[cat1, 5], [cat2, null]], 400, "Invalid score: None");
    post("Too low", [[cat1, 0]], 400, "Invalid score: 0");
    post("Too high", [[cat1, 16]], 400, "Invalid score: 16");
    post("Multi Scores", [[cat1, 5], [cat2, 5]], 200, "Score entered for " +
        p1 + ": 5\nScore entered for " + p1 + ": 5");
    post("Enter twice", [[cat1, 5]], 200, "Score entered for " + p1);
    post("Change", [[cat1, 4]], 400, "4 not entered. Score is already set");
    post("Enter twice as string", [[cat2, '5']], 200, "Score entered for " + p1);
    post("Fake category", [["non_", 5]], 400, "Unknown category: non_");
});
