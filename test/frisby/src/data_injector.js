/* Helper methods to inject data via the daoserver */
var frisby = require("frisby");

var auth = function(user, pass) {
        return "Basic " + new Buffer(user + ":" + pass).toString("base64");
    };

// Inserts a new tournament
exports.createTournament = function(tournament, date) {
    "use strict";
    var API = process.env.API_ADDR + "tournament",
        to = tournament + "_to",
        postData = {
            inputTournamentName: tournament,
            inputTournamentDate: date
        };

    exports.createUser(to);

    frisby.create("Insert tournament: " + tournament)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", auth(to, "password"))
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
        .addHeader("Authorization", auth(username, "password"))
        .expectStatus(200)
        .toss();
};

// Set the score categories
exports.setCategories = function(tourn, categories){
    "use strict";

    var API = process.env.API_ADDR + "tournament/" + tourn + "/score_categories",
        postData = {score_categories: []};

    categories.forEach(function(cat){
        postData.score_categories.push({
            "name": cat[0],
            "percentage": cat[1],
            "per_tournament": cat[2],
            "min_val": cat[3],
            "max_val": cat[4],
            "zero_sum": cat[5] || false,
            "opponent_score": cat[6] || false
            });
    });

    frisby.create("set the score categories for " + tourn)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", auth("superuser", "password"))
        .expectStatus(200)
        .toss();
};

// Set missions
exports.setMissions = function(tourn, missions){
    "use strict";
    var API = process.env.API_ADDR + "tournament/" + tourn + "/missions";

    frisby.create("POST " + missions.length + " missions to setup")
        .post(API, {missions: missions}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", auth("superuser", "password"))
        .expectStatus(200)
        .toss();
};

// Set number of rounds for a tournament
exports.postRounds = function(tourn, rounds) {
    "use strict";

    var API = process.env.API_ADDR + "tournament/" + tourn + "/rounds";
    frisby.create("POST " + rounds + " rounds to setup")
        .post(API, {numRounds: rounds}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", auth("superuser", "password"))
        .expectStatus(200)
        .toss();
};
