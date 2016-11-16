var frisby = require("frisby"),
    utils = require("./utils"),
    API = process.env.API_ADDR + "tournament/category_test/categories";

describe("No auth", function () {
    "use strict";
    frisby.create("no auth for categories page")
        .get(API)
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("No auth for categories page content")
        .get(API + "/content")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();
});

describe("Bad path", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Non-existent tournament content")
            .get(process.env.API_ADDR + "tournament/foo/categories/content")
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Tournament foo not found in database"})
            .toss();
        });
});

describe("Get categories", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Categories page content")
            .get(API + "/content", {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                instructions: "Set the score categories for category_test " +
                    "here. For example, \"Battle\", \"Sports\", etc.",
                tournament: "category_test",
                categories: [
                    {   name: "category_1",
                        opponent_score: false,
                        zero_sum: false,
                        min_val: 1,
                        max_val: 10,
                        per_tournament: false,
                        percentage: 15,
                        id: 10 },
                    {   name: "",
                        percentage: "",
                        per_tournament: false,
                        min_val: "",
                        max_val: "",
                        zero_sum: false,
                        opponent_score: false },
                    {   name: "",
                        percentage: "",
                        per_tournament: false,
                        min_val: "",
                        max_val: "",
                        zero_sum: false,
                        opponent_score: false },
                    {   name: "",
                        percentage: "",
                        per_tournament: false,
                        min_val: "",
                        max_val: "",
                        zero_sum: false,
                        opponent_score: false },
                    {   name: "",
                        percentage: "",
                        per_tournament: false,
                        min_val: "",
                        max_val: "",
                        zero_sum: false,
                        opponent_score: false }
                    ]
                })
            .toss();
        });
});

describe("Set categories", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        var details = {
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
            };

        frisby.create("Categories page content")
            .post(API, details)
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({message: "Tournament category_test updated"})
            .toss();
        });
});

describe("Empty categories", function () {
    "use strict";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Categories page content")
            .post(API, {})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({message: "Tournament category_test updated"})
            .toss();
        });
});

describe("Duplicate categories", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {
        var details = {
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
                    name: "foo",
                    percentage: 10,
                    per_tournament: false,
                    zero_sum: false,
                    opponent_score: false,
                    min_val: 10,
                    max_val: 10
                }]
            };

        frisby.create("post duplicate categories")
            .post(API, details)
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({
                error: "You cannot set multiple keys with the same name"})
            .toss();
        });
});

describe("Illegal category", function () {
    "use strict";

    utils.asUser("superman", "password", function(cookie) {
        var details = {
            categories: [{
                name: "foo",
                percentage: 101,
                per_tournament: false,
                zero_sum: false,
                opponent_score: false,
                min_val: 10,
                max_val: 10
                }]
            };

        frisby.create("post illegal category")
            .post(API, details)
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Percentage must be an integer (1-100)"})
            .toss();
        });
});
