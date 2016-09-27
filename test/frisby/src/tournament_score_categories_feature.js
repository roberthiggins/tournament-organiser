var frisby = require("frisby"),
    injector = require("./data_injector.js"),
    API = process.env.API_ADDR +
            "tournament/category_test/score_categories";

describe("Set categories normal function", function () {
    "use strict";

    injector.setCategories("category_test", [
        ["categories_test_one", 8, true, 4, 12],
        ["categories_test_two", 13, false, 3, 11]]);
    frisby.create("GET a list of tournament categories")
        .get(API)
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes("0", {
            "id": Number,
            "name": String,
            "percentage": Number,
            "per_tournament": Boolean,
            "min_val": Number,
            "max_val": Number
        })
        .expectJSON([
            {
                "id": Number,
                "name": "categories_test_one",
                "percentage": 8,
                "per_tournament": true,
                "min_val": 4,
                "max_val": 12
            },
            {
                "id": Number,
                "name": "categories_test_two",
                "percentage": 13,
                "per_tournament": false,
                "min_val": 3,
                "max_val": 11
            }
        ])
        .toss();


    // Modify the categories
    frisby.create("set the score categories for category_test")
        .post(API, {
            categories: ["categories_3"],
            categories_3: ["categories_test_three", 99, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", "Basic " +
            new Buffer("category_test_to:password").toString("base64"))
        .expectStatus(200)
        .toss();
    frisby.create("GET a list of tournament categories")
        .get(API)
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([
            {
                "id": Number,
                "name": "categories_test_three",
                "percentage": 99,
                "per_tournament": true,
                "min_val": 1,
                "max_val": 2
            }
        ])
        .toss();

    frisby.create("set the score categories for category_test to none")
        .post(API, {
            categories: []
        }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", "Basic " +
            new Buffer("category_test_to:password").toString("base64"))
        .expectStatus(200)
        .toss();
});

describe("Set categories malformed", function () {
    "use strict";

    frisby.create("GET from non-existent tournament")
        .get(process.env.API_ADDR + "tournament/not_a_thing/score_categories")
        .expectStatus(400)
        .toss();

    frisby.create("GET from non-existent tournament")
        .get(process.env.API_ADDR + "tournament//score_categories")
        .expectStatus(404)
        .toss();

    // Empty the categories
    frisby.create("set the score categories for category_test to none")
        .post(API, {
            categories: []
        }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", "Basic " +
            new Buffer("category_test_to:password").toString("base64"))
        .expectStatus(200)
        .toss();
    frisby.create("GET categories from now empty tournament")
        .get(API)
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([])
        .toss();


    // Modify the categories incorrectly
    frisby.create("Incorrect: categories don\"t match")
        .post(API, {
            categories: ["categories_3"],
            categories_1: ["categories_test_no_match", 5, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create("Incorrect: No names")
        .post(API, {
            categories_1: ["categories_test_no_names", 5, true, 1, 2]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create("Incorrect: No category info")
        .post(API, {
            categories: ["categories_3"]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
});

describe("Set categories permissions", function () {
    "use strict";

    injector.createUser("category_test_player_1");
    injector.enterTournament("category_test", "category_test_player_1");

    var authTestCategories = function(msg, user, code){
            frisby.create("POST categories as: " + msg)
                .post(API, {categories: []}, {json: true})
                .addHeader("Authorization", "Basic " +
                    new Buffer(user + ":password").toString("base64"))
                .expectStatus(code)
                .toss();
        };
    authTestCategories("TO", "category_test_to", 200);
    authTestCategories("Non user", "fadsfdsfasdfasdf", 401);
    authTestCategories("Other user", "rank_test_player_1", 403);
    authTestCategories("Player", "category_test_player_1", 403);
    authTestCategories("Super", "superuser", 200);
    frisby.create("set the score categories with no auth")
        .post(API, {categories: []}, {json: true})
        .expectStatus(401)
        .toss();
});
