describe("Test seeing and registering for a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        API = process.env.API_ADDR + "tournament/",
        injector = require("./data_injector"),
        asJSON = function(date, entries, name, rounds) {
            return {
                date: date,
                entries: entries,
                name: name,
                rounds: rounds
            };
        };

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
                entries: Number,
                name: String,
                rounds: Number
            })
        .expectJSON("tournaments", [
            asJSON("1985-01-27", 5, "draw_test",             2),
            asJSON("2095-10-10", 2, "enter_score_test",      1),
            asJSON("2095-07-02", 1, "entry_info_test",       0),
            asJSON("2095-07-03", 2, "entry_list_test",       0),
            asJSON("2095-07-04", 0, "entry_list_test_empty", 0),
            asJSON("2095-07-01", 1, "mission_test",          3),
            asJSON("2095-08-12", 5, "next_game_test",        2),
            asJSON("2432-03-17", 0, "no_rounds_test",        0),
            asJSON("2095-06-01", 0, "northcon_2095",         0),
            asJSON("2095-07-06", 1, "permission_test",       0),
            asJSON("1643-01-27", 5, "rank_test",             2),
            asJSON("2222-06-01", 0, "register_test",         0),
            asJSON("2095-07-07", 0, "round_test",            2),
            asJSON("2163-09-15", 5, "schedule_test",         2),
            asJSON("2063-03-17", 3, "start_test",            1),
            asJSON("9999-12-31", 0, "t_create_test",         3)])
        .toss();

    frisby.create("enter a user")
        .post(API + "register_test/register/register_test_player_1")
        .addHeader("Authorization", injector.auth("register_test_player_1"))
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
        .addHeader("Authorization", injector.auth("register_test_player_1"))
        .expectStatus(400)
        .expectBodyContains("You've already applied to register_test")
        .toss();

    frisby.create("enter a user as someone else")
        .post(API + "register_test/register/register_test_player_2")
        .addHeader("Authorization", injector.auth("register_test_player_1"))
        .expectStatus(403)
        .expectBodyContains("Permission denied")
        .toss();

    frisby.create("enter user as superuser")
        .post(API + "register_test/register/register_test_player_2")
        .addHeader("Authorization", injector.auth("superuser"))
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
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(400)
        .expectBodyContains("Check username and tournament")
        .toss();

    frisby.create("malformed")
        .post(API + "register_test/register")
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(404)
        .toss();
});
