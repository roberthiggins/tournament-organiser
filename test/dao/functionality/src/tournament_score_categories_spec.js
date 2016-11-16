var frisby = require("frisby"),
    injector = require("./data_injector.js");

describe("Empty categories", function () {
    "use strict";

    var tourn = "category_test_1",
        API = process.env.API_ADDR + "tournament/" + tourn;

    injector.createTournament(tourn, "2095-07-05", null, null,
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

    frisby.create("set the score categories to none")
        .post(API, {
            score_categories: []
        }, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(tourn + "_to"))
        .expectStatus(200)
        .after(function(){
            frisby.create("GET categories from now empty tournament")
                .get(API + "/score_categories")
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSON([])
                .toss();
            })
        .toss();
});

describe("Set categories normal function", function () {
    "use strict";
    var tourn = "category_test_2",
        API = process.env.API_ADDR + "tournament/" + tourn;

    injector.createTournament(tourn, "2095-07-05", null, null,
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

    frisby.create("set the score categories for " + tourn)
        .post(API, {
            score_categories: [
                injector.jsonCat(null, "cat_t_three", 99, true, 1, 2, false,
                    false)
                ]}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(tourn + "_to"))
        .expectStatus(200)
        .after(function() {
            frisby.create("Categories should now have one category")
                .get(API + "/score_categories")
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSON([injector.jsonCat(Number, "cat_t_three", 99, true,
                    1, 2, false, false)])
                .toss();
            })
        .toss();
});

describe("Set categories malformed", function () {
    "use strict";

    var tourn = "category_test_1",
        API = process.env.API_ADDR + "tournament/" + tourn;

    frisby.create("GET from non-existent tournament")
        .get(process.env.API_ADDR + "tournament/not_a_thing/score_categories")
        .expectStatus(400)
        .toss();

    frisby.create("GET from non-existent tournament")
        .get(process.env.API_ADDR + "tournament//score_categories")
        .expectStatus(404)
        .toss();

    frisby.create("Incorrect: duplicate")
        .post(API, {
            score_categories: [
                injector.jsonCat(null, "cat_t_zero", 10, true, 1, 2, false,
                    false),
                injector.jsonCat(null, "cat_t_zero", 10, true, 1, 2, false,
                    false)
                ]}, {json: true, inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(tourn + "_to"))
        .expectStatus(400)
        .expectBodyContains("You cannot set multiple keys with the same name")
        .toss();
});

describe("Set categories permissions", function () {
    "use strict";

    var tourn = "category_test_1",
        API = process.env.API_ADDR + "tournament/" + tourn,
        player = tourn + "_player_1";

    injector.createUser(player);
    injector.enterTournament(tourn, player);

    var authTestCategories = function(msg, user, code){
            frisby.create("POST categories as: " + msg)
                .post(API, {score_categories: []}, {json: true})
                .addHeader("Authorization", injector.auth(user))
                .expectStatus(code)
                .toss();
        };
    authTestCategories("TO", tourn + "_to", 200);
    authTestCategories("Non user", "fadsfdsfasdfasdf", 401);
    authTestCategories("Other user", "rank_test_player_1", 403);
    authTestCategories("Player", player, 403);
    authTestCategories("Super", "superuser", 200);
    frisby.create("set the score categories with no auth")
        .post(API, {categories: []}, {json: true})
        .expectStatus(401)
        .toss();
});
