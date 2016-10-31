var frisby = require("frisby"),
    API = process.env.API_ADDR + "tournament",
    injector = require("./data_injector"),
    category = injector.jsonCat(null, "cat_t_three", 99, true, 1, 2, false,
                false),
    date = "9999-12-31",
    rounds = 3,
    tourn = "t_create_test",
    to = tourn + "_to",
    postData = {
        inputTournamentName: tourn,
        inputTournamentDate: date,
        rounds: rounds,
        score_categories: [category]
    };

(function setup() {
    injector.createUser(to);
})();

describe("Tournament creation auth", function() {
    "use strict";
    frisby.create("Insert tournament without auth: " + tourn)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .expectStatus(401)
        .toss();
});

describe("Test tournament creation with bad values", function () {
    "use strict";
    var noName = {
        inputTournamentDate: date,
        rounds: rounds,
        score_categories: [category]
        };
    frisby.create("Insert tournament without name: " + tourn)
        .post(API, noName, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(to))
        .expectStatus(400)
        .toss();

    var noDate = {
        inputTournamentName: tourn,
        rounds: rounds,
        score_categories: [category]
        };

    frisby.create("Insert tournament without date: " + tourn)
        .post(API, noDate, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(to))
        .expectStatus(400)
        .toss();

});

describe("Test tournament creation", function () {
    "use strict";

    frisby.create("Insert tournament: " + tourn)
        .post(API, postData, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(to))
        .expectStatus(200)
        .expectJSONTypes({
            date: String,
            name: String,
            rounds: Number,
            score_categories: Array
            })
        .expectJSON({
            date: date,
            name: tourn,
            rounds: rounds,
            score_categories: [category]
            })
        .after(function() {
            frisby.create("See a list of tournaments")
                .get(API, {inspectOnFailure: true})
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSONTypes({tournaments: Array})
                .expectJSONTypes("tournaments.0",
                    {
                        date: String,
                        name: String,
                        rounds: Number
                    })
                .expectJSON("tournaments.?",
                    {date: date, name: tourn, rounds: rounds})
                .toss();
            })
        .toss();
});
