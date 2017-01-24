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
        emptyScore = {
            scores: [
                {
                    score: '',
                    category: cat
                }
            ]
        },
        emptyCat = {
            scores: [
                {
                    score: 1,
                    category: ''
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
        nothing = {};

    post("No cat",      noCat,      "Unknown category: None");
    post("No score",    noScore,    "Invalid score: None");
    post("Keys only",   keysOnly,   "Invalid score: None");
    post("Empty score", emptyScore, "Invalid score: ");
    post("Empty cat",   emptyCat,   "Unknown category: ");
    post("No keys",     noKeys,     "Invalid score: None");
    post("No Scores",   noScores,   "Invalid score: None");
    post("Empty dict",  nothing,    "Invalid score: None");
});
