var frisby = require("frisby"),
    injector = require("./data_injector.js"),
    API = process.env.API_ADDR + "tournament/category_test";

describe("Set categories normal function", function () {
    "use strict";

    injector.createTournament("category_test", "2095-07-05", null, null,
        [["cat_t_one", 8, true, 4, 12, false, false],
         ["cat_t_two", 13, false, 3, 11, true, true]]);
    frisby.create("GET a list of tournament categories")
        .get(API + "/score_categories")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes("0", {
            "id": Number,
            "name": String,
            "percentage": Number,
            "per_tournament": Boolean,
            "min_val": Number,
            "max_val": Number,
            "zero_sum": Boolean,
            "opponent_score": Boolean
        })
        .expectJSON([
            injector.jsonCat(Number, "cat_t_one", 8, true, 4, 12, false, false),
            injector.jsonCat(Number, "cat_t_two", 13, false, 3, 11, true, true)
        ])
        .toss();


    // Modify the categories
    frisby.create("set the score categories for category_test")
        .post(API, {
            categories: ["categories_3"],
            categories_3:
                injector.jsonCat(null, "cat_t_three", 99, true, 1, 2, false,
                    false)
            }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", "Basic " +
            new Buffer("category_test_to:password").toString("base64"))
        .expectStatus(200)
        .after(function() {
            frisby.create("GET a list of tournament categories")
                .get(API + "/score_categories")
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSON([injector.jsonCat(Number, "cat_t_three", 99, true,
                    1, 2, false, false)])
                .toss();
            })
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
        .get(API + "/score_categories")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([])
        .toss();


    // Modify the categories incorrectly
    frisby.create("Incorrect: categories don\"t match")
        .post(API, {
            categories: ["categories_3"],
            categories_1:
                injector.jsonCat(null, "cat_t_no_match", 5, true, 1, 2, false,
                    false)
            }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create("Incorrect: No names")
        .post(API, {
            categories_1:
                injector.jsonCat(null, "cat_t_no_names", 5, true, 1, 2, false,
                    false)
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();
    frisby.create("Incorrect: No category info")
        .post(API, {
            categories: ["categories_3"]
        }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .toss();

    frisby.create("Incorrect: duplicate")
        .post(API, {
            categories: ["categories_0", "categories_1"],
            categories_0:
                injector.jsonCat(null, "cat_t_zero", 10, true, 1, 2, false,
                    false)
            categories_1:
                injector.jsonCat(null, "cat_t_one", 10, true, 1, 2, false,
                    false)
            }, {json: true, inspectOnFailure: true})
        .expectStatus(400)
        .expectJSON({error: "multiple"})
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
