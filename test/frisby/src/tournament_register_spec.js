describe("Test seeing and registering for a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        API = process.env.API_ADDR + "tournament/",
        injector = require("./data_injector");

    injector.createTournament("register_test", "2222-06-01");
    injector.createUser("register_test_player_1");
    injector.createUser("register_test_player_2");

    frisby.create("See upcoming tournaments")
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
        .expectJSON("tournaments", [
            {date: "1985-01-27", name: "draw_test",             rounds: 2},
            {date: "2095-10-10", name: "enter_score_test",      rounds: 1},
            {date: "2095-07-02", name: "entry_info_test",       rounds: 0},
            {date: "2095-07-03", name: "entry_list_test",       rounds: 0},
            {date: "2095-07-04", name: "entry_list_test_empty", rounds: 0},
            {date: "2095-07-01", name: "mission_test",          rounds: 3},
            {date: "2095-08-12", name: "next_game_test",        rounds: 2},
            {date: "2432-03-17", name: "no_rounds_test",        rounds: 0},
            {date: "2095-06-01", name: "northcon_2095",         rounds: 0},
            {date: "2095-07-06", name: "permission_test",       rounds: 0},
            {date: "1643-01-27", name: "rank_test",             rounds: 2},
            {date: "2222-06-01", name: "register_test",         rounds: 0},
            {date: "2095-07-07", name: "round_test",            rounds: 2},
            {date: "2163-09-15", name: "schedule_test",         rounds: 2},
            {date: "2063-03-17", name: "start_test",            rounds: 1},
            {date: "9999-12-31", name: "t_create_test",         rounds: 3}])
        .toss();

    frisby.create("enter a user")
        .post(API + "register_test/register/register_test_player_1")
        .addHeader("Authorization", "Basic " +
            new Buffer("register_test_player_1:password").toString("base64"))
        .expectStatus(200)
        .expectBodyContains("Application Submitted")
        .after(function(){
            frisby.create("check they are entered")
                .get(API + "register_test/entry/")
                .expectStatus(200)
                .expectJSON(["register_test_player_1"])
                .toss();
        })
        .toss();

    frisby.create("enter a user a second time")
        .post(API + "register_test/register/register_test_player_1")
        .addHeader("Authorization", "Basic " +
            new Buffer("register_test_player_1:password").toString("base64"))
        .expectStatus(400)
        .expectBodyContains("You've already applied to register_test")
        .toss();

    frisby.create("enter a user as someone else")
        .post(API + "register_test/register/register_test_player_2")
        .addHeader("Authorization", "Basic " +
            new Buffer("register_test_player_1:password").toString("base64"))
        .expectStatus(403)
        .expectBodyContains("Permission denied")
        .toss();

    frisby.create("enter user as superuser")
        .post(API + "register_test/register/register_test_player_2")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(200)
        .expectBodyContains("Application Submitted")
        .after(function(){
            frisby.create("check they are entered")
                .get(API + "register_test/entry/")
                .expectStatus(200)
                .expectJSON(
                    ["register_test_player_1", "register_test_player_2"])
                .toss();
        })
        .toss();

    frisby.create("enter a non-user")
        .post(API + "register_test/register/noone")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(400)
        .expectBodyContains("Check username and tournament")
        .toss();

    frisby.create("malformed")
        .post(API + "register_test/register")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(404)
        .toss();
});
