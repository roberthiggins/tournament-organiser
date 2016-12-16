var frisby = require("frisby"),
    utils = require("./utils"),
    API = process.env.API_ADDR + "tournament/create";

describe("Auth", function () {
    "use strict";
    frisby.create("no auth for creation page page")
        .get(API)
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("logged in")
            .get(API)
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectBodyContains("tournamentCreate.js")
            .toss();
        });
});

describe("Create a tournament", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {

        var allValues = {
                name: "test_tournament_creation",
                date: "9999-12-31",
                rounds: 1,
                categories: [
                    {
                        name: "foo",
                        percentage: 10,
                        per_tournament: false,
                        zero_sum: false,
                        opponent_score: false,
                        min_val: 10,
                        max_val: 10
                    },
                    {
                        name: "bar",
                        percentage: 10,
                        per_tournament: false,
                        zero_sum: false,
                        opponent_score: false,
                        min_val: 10,
                        max_val: 10
                    }]
                },
            minValues = {
                name: "test_tournament_creation_2",
                date: "9999-12-31"
                };

        frisby.create("All the values")
            .post(API, allValues, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                date: "9999-12-31",
                score_categories: [
                    {   name: "foo",
                        opponent_score: false,
                        zero_sum: false,
                        min_val: 10,
                        max_val: 10,
                        per_tournament: false,
                        percentage: 10,
                        id: Number },
                    {   name: "bar",
                        opponent_score: false,
                        zero_sum: false,
                        min_val: 10,
                        max_val: 10,
                        per_tournament: false,
                        percentage: 10,
                        id: Number }
                    ],
                rounds: 1,
                name: "test_tournament_creation",
                entries: 0
                })
            .toss();

        frisby.create("Minimum values")
            .post(API, minValues, {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                date: "9999-12-31",
                score_categories: [],
                rounds: 0,
                name: "test_tournament_creation_2",
                entries: 0
                })
            .toss();
        });
});

describe("Bad Values", function () {
    "use strict";

    frisby.create("No auth")
        .post(API, {name: "foo", date: "2095-01-01"},
            {json: true, inspectOnFailure: true})
        .expectStatus(302)
        .toss();

    utils.asUser("superman", "password", function(cookie) {

        frisby.create("No name")
            .post(API, {name: "", date: "2095-01-01"},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Enter a valid name"})
            .toss();

        frisby.create("No date")
            .post(API, {name: "red", date: ""},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Enter a valid date"})
            .toss();

        var name = "creation_test_3";
        frisby.create("Duplicate")
            .post(API, {name: name, date: "2095-01-01"},
                {json: true, inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .after(function() {
                frisby.create("Duplicate")
                    .post(API, {name: name, date: "2095-01-01"},
                        {json: true, inspectOnFailure: true})
                    .addHeader("cookie", cookie)
                    .expectStatus(400)
                    .expectJSON({error: "A tournament with name " + name +
                        " already exists! Please choose another name"})
                    .toss();
                })
            .toss();
        });
});
