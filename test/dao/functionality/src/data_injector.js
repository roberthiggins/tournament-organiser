/* Helper methods to inject data via the daoserver */
var frisby = require("frisby");

exports.auth = function(user, password) {
        var pass = password || "password";
        return "Basic " + new Buffer(user + ":" + pass).toString("base64");
    };

var postCategory = function(cat){
    return {
        "name": cat[0],
        "percentage": cat[1],
        "per_tournament": cat[2],
        "min_val": cat[3],
        "max_val": cat[4],
        "zero_sum": cat[5] || false,
        "opponent_score": cat[6] || false
        };
};

// Inserts a new tournament
exports.createTournament = function(tournament, date, rounds, missions,
    scoreCategories, players) {
    "use strict";
    var API = process.env.API_ADDR + "tournament",
        to = tournament + "_to",
        categories = (scoreCategories || []).map(function(cat){
            return postCategory(cat);
            }),
        postData = {
            inputTournamentName: tournament,
            inputTournamentDate: date,
            rounds: rounds || 0,
            missions: missions,
            score_categories: categories
        };

    exports.createUser(to);

    frisby.create("Insert tournament: " + tournament)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth(to))
        .expectStatus(200)
        .toss();

    (players || []).forEach(function(player) {
        exports.createUser(player);
        exports.enterTournament(tournament, player);
        });
};


// Insert a new user
exports.createUser = function(username) {
    "use strict";
    var API = process.env.API_ADDR + "user/" + username,
        postData = {
            email: username + "@bar.com",
            password1: "password",
            password2: "password"
        };

    frisby.create("Insert user: " + username)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .toss();
};

// Enter user into tournament
exports.enterTournament = function(tournament, username) {
    "use strict";
    var API = process.env.API_ADDR + "tournament/" + tournament + "/register/" +
                username;
    frisby.create("Add user " + username + " to " + tournament)
        .post(API, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth(username))
        .expectStatus(200)
        .toss();
};

// Enter a score. You can specify a response code and message
exports.enterScore = function(per_tourn, tourn, player, user, msg, scores, code,
    resp, gameId){

    var append = per_tourn ? "_per_tourn_1" : "_per_game_1",
        API = process.env.API_ADDR + "tournament/" + tourn + "/entry/" +
            player,
        postScore = function (gameId){
            var postData = {
                scores: scores.map(function(pair){
                    var category = pair[0] ? pair[0] : tourn + append;
                    return {
                        game_id: gameId,
                        category: category,
                        score: pair[1]
                        };
                    })
                },
                req = frisby.create("POST score: " + msg)
                    .post(API + "/score", postData,
                        {json: true, inspectOnFailure: true})
                    .expectStatus(code)
                    .expectBodyContains(resp);

                if (user) {
                    req.addHeader("Authorization", exports.auth(user));
                }

                req.toss();
            };

    if (per_tourn) {
        postScore();
    }
    else if (gameId) {
        postScore(gameId);
    }
    else {
        frisby.create("get game_id of next game for " + user)
            .get(API + "/nextgame")
            .expectStatus(200)
            .afterJSON(function (body) { postScore(body.game_id); })
            .toss();
    }
};

// A json blob for a single score category
exports.jsonCat = function(id, name, pct, per_tourn, min, max, z_sum, opp) {
    var cat = {
        name: name,
        percentage: pct,
        per_tournament: per_tourn,
        min_val: min,
        max_val: max,
        zero_sum: z_sum,
        opponent_score: opp
        };
    if (id) {
        cat.id = id;
    }
    return cat;
};

// Set number of rounds for a tournament
exports.postRounds = function(tourn, rounds) {
    "use strict";

    var API = process.env.API_ADDR + "tournament/" + tourn;
    frisby.create("POST " + rounds + " rounds to setup")
        .post(API, {rounds: rounds}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth("superuser"))
        .expectStatus(200)
        .toss();
};
