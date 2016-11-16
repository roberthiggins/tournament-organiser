var frisby = require("frisby"),
    utils = require("./utils");

describe("Tournament List", function () {
    "use strict";
    frisby.create("Tournament List Page")
        .get(process.env.API_ADDR + "tournaments")
        .expectStatus(200)
        .toss();

    frisby.create("Tournament List Content")
        .get(process.env.API_ADDR + "tournaments/content")
        .expectStatus(200)
        .expectJSONTypes({tournaments: Array})
        .expectJSONTypes("tournaments.0", {
            date: String,
            user_entered: Boolean,
            rounds: Number,
            name: String,
            entries: Number
            })
        .expectJSON("tournaments.?", {
            date: "2095-07-12",
            user_entered: false,
            rounds: 0,
            name: "category_test",
            entries: 0
            })
        .toss();
});

describe("Tournament", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/";

    frisby.create("Individual Tournament Page")
        .get(API + "ranking_test")
        .expectStatus(200)
        .toss();

    frisby.create("Non-existent Tournament Page")
        .get(API + "not_a_tournament")
        .expectStatus(200)
        .toss();

    frisby.create("Tournament Details content")
        .get(API + "painting_test/content")
        .expectStatus(200)
        .expectJSONTypes({
            date: String,
            entries: Number,
            name: String,
            rounds: Number,
            score_categories: Array,
            user_entered: Boolean
            })
        .expectJSONTypes("score_categories.0", {
            name: String,
            opponent_score: Boolean,
            zero_sum: Boolean,
            min_val: Number,
            max_val: Number,
            per_tournament: Boolean,
            percentage: Number,
            id: Number 
            })
        .expectJSON({
            date: "2095-10-10",
            entries: 2,
            name: "painting_test",
            rounds: 0,
            score_categories: [{
                name: "Fanciness",
                opponent_score: false,
                zero_sum: false,
                min_val: 4,
                max_val: 15,
                per_tournament: true,
                percentage: 10,
                }],
            user_entered: false
            })
        .toss();

    frisby.create("Content for non-existent tournament")
        .get(API + "not_a_tourn/content")
        .expectStatus(400)
        .expectJSONTypes({error: String})
        .expectJSON({error: "Tournament not_a_tourn not found in database"})
        .toss();
});

describe("Tournament Entries", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/";

    frisby.create("Tournament Entries")
        .get(API + "ranking_test/entries")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    utils.asUser("superman", "password", function(cookie) {

        frisby.create("Tournament with no entries")
            .get(API + "empty_tournament/entries/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                entries: [],
                tournament: "empty_tournament"
                })
            .toss();

        frisby.create("Tournament Details Content")
            .get(API + "ranking_test/entries/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                entries: [
                    "ranking_test P1",
                    "ranking_test_player_2",
                    "ranking_test_player_3",
                    "ranking_test_player_4",
                    "ranking_test_player_5"
                    ],
                tournament: "ranking_test"
                })
            .expectJSONTypes({
                entries: Array,
                tournament: String
                })
            .toss();
        });
});

describe("Non-Existent Tournament Entries", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/";

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Non-existent Tournament Entries")
            .get(API + "not_a_tourn/entries")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .toss();

        frisby.create(" Content")
            .get(API + "not_a_tourn/entries/content")
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSONTypes({error: String})
            .expectJSON({error: "Tournament not_a_tourn doesn't exist"})
            .toss();
        });
});
