var frisby = require("frisby"),
    injector = require("./data_injector"),
    API = process.env.API_ADDR;

describe("Test get draw", function () {
    "use strict";
    var tourn = "no_rounds_test";

    injector.createTournament(tourn, "2432-03-17", null, null,
        [["cat_1", 8, true, 4, 12, false, false]]);


    frisby.create("Check draw for tournament with no rounds")
        .get(API + "tournament/" + tourn + "/rounds/1")
        .expectStatus(400)
        .expectBodyContains("Tournament " + tourn + " does not have a round 1")
        .toss();

    frisby.create("Check the draw")
        .get(API + "tournament/draw_test/rounds/1")
        .expectStatus(200)
        .expectJSON({
            draw: Array,
            mission: String
        })
        .toss();
});


describe("Start the tournament", function () {
    "use strict";
    var tourn = "start_test";

    injector.createTournament(tourn, "2063-03-17", 1, ["Mission the First"],
        [["cat_1", 8, true, 4, 12, false, false]]);

    // Test people forcing a draw manually
    injector.createUser("start_test_player_1");
    injector.createUser("start_test_player_2");
    injector.createUser("start_test_player_3");
    injector.createUser("start_test_non_player");
    injector.enterTournament(tourn, "start_test_player_1");
    injector.enterTournament(tourn, "start_test_player_2");

    frisby.create("Begin tournament as player")
        .post(API + "tournament/" + tourn + "/start")
        .expectStatus(403)
        .addHeader("Authorization", "Basic " +
            new Buffer("start_test_player_1:password").toString("base64"))
        .toss();
    frisby.create("Begin tournament as another user")
        .post(API + "tournament/" + tourn + "/start")
        .expectStatus(403)
        .addHeader("Authorization", "Basic " +
            new Buffer("start_test_non_player:password").toString("base64"))
        .toss();
    frisby.create("Begin tournament as nobody")
        .post(API + "tournament/" + tourn + "/start")
        .expectStatus(401)
        .addHeader("Authorization", "Basic " +
            new Buffer("non_player:password").toString("base64"))
        .toss();


    // We should be able to add player 3
    injector.enterTournament(tourn, "start_test_player_3");

    // Then begin the tournament
    frisby.create("Begin tournament as TO")
        .post(API + "tournament/" + tourn + "/start")
        .expectStatus(200)
        .addHeader("Authorization", "Basic " +
            new Buffer("start_test_to:password").toString("base64"))
        .toss();

    // We can no longer enter players
    frisby.create("Can no longer enter players")
        .post(API + "tournament/" + tourn + "/register/start_test_non_player")
        .addHeader("Authorization", "Basic " +
            new Buffer("start_test_non_player:password").toString("base64"))
        .expectStatus(400)
        .expectBodyContains("You cannot perform this action on a tournament that is in progress")
        .toss();
});
