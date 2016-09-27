/* Helper methods to inject data via the daoserver */
var frisby = require("frisby");

var auth = function(user, pass) {
        return "Basic " + new Buffer(user + ":" + pass).toString("base64");
    };

// Set the score categories
exports.setCategories = function(tourn, categories){
    "use strict";

    var API = process.env.API_ADDR + "tournament/" + tourn + "/score_categories",
        postData = {categories: []};

    categories.forEach(function(cat, idx){
        var key = "categories_" + idx;
        postData.categories.push(key);
        postData[key] = cat;
    });

    frisby.create("set the score categories for " + tourn)
        .post(API, postData, {json: true, inspectOnFailure: true})
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
