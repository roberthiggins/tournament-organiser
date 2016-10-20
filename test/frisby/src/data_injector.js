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
    scoreCategories) {
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
            missions: missions || [],
            score_categories: categories
        };

    exports.createUser(to);

    frisby.create("Insert tournament: " + tournament)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth(to))
        .expectStatus(200)
        .toss();
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

// A json blob for a single score category
exports.jsonCat = function(id, name, pct, per_tourn, min, max, z_sum, opp) {
    var cat = {
        "name": name,
        "percentage": pct,
        "per_tournament": per_tourn,
        "min_val": min,
        "max_val": max,
        "zero_sum": z_sum,
        "opponent_score": opp
        };
    if (id) {
        cat.id = id;
    }
    return cat;
};

// Set the score categories
exports.setCategories = function(tourn, categories){
    "use strict";

    var API = process.env.API_ADDR + "tournament/" + tourn + "/score_categories",
        postData = {score_categories: []};

    categories.forEach(function(cat){
        postData.score_categories.push(postCategory(cat));
    });

    frisby.create("set the score categories for " + tourn)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth("superuser"))
        .expectStatus(200)
        .toss();
};

// Set missions
exports.setMissions = function(tourn, missions){
    "use strict";
    var API = process.env.API_ADDR + "tournament/" + tourn + "/missions";

    frisby.create("POST " + missions.length + " missions to setup")
        .post(API, {missions: missions}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", exports.auth("superuser"))
        .expectStatus(200)
        .toss();
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
