describe("Test seeing and registering for a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        API = process.env.API_ADDR + "tournament/",
        injector = require("./data_injector"),
        asJSON = function(date, entries, name, rounds, userEntered) {
            return {
                date: date,
                entries: entries,
                name: name,
                rounds: rounds,
                user_entered: userEntered
            };
        },
        tourn_1 = "register_test_1",
        tourn_2 = "register_test_2",
        player_1 = "register_test_player_1",
        player_2 = "register_test_player_2";

    injector.createTournament(tourn_1, "2222-06-01");
    injector.createTournament(tourn_2, "2222-06-02", null, null, null,
        [player_1]);
    injector.createUser(player_2);

    frisby.create("See upcoming tournaments")
        .get(API, {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(player_1))
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes({tournaments: Array})
        .expectJSONTypes("tournaments.0",
            {
                date: String,
                entries: Number,
                name: String,
                rounds: Number,
                user_entered: Boolean
            })
        .expectJSON("tournaments", [
            asJSON("1985-01-27", 5, "draw_test",             2, false),
            asJSON("2095-07-01", 0, "empty_tournament",      0, false),
            asJSON("2095-10-10", 2, "enter_score_test_0",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_1",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_2",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_3",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_4",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_5",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_6",    1, false),
            asJSON("2095-10-10", 2, "enter_score_test_7",    1, false),
            asJSON("2095-07-02", 1, "entry_info_test",       0, false),
            asJSON("2095-07-03", 2, "entry_list_test",       0, false),
            asJSON("2095-07-04", 0, "entry_list_test_empty", 0, false),
            asJSON("2095-07-01", 1, "mission_test",          3, false),
            asJSON("2095-08-12", 5, "next_game_test",        2, false),
            asJSON("2432-03-17", 0, "no_rounds_test",        0, false),
            asJSON("2095-06-01", 0, "northcon_2095",         0, false),
            asJSON("2095-07-06", 1, "permission_test",       0, false),
            asJSON("1643-01-27", 5, "rank_test",             2, false),
            asJSON("2222-06-01", 0, tourn_1,                 0, false),
            asJSON("2222-06-02", 1, tourn_2,                 0, true),
            asJSON("2095-07-07", 0, "round_test",            2, false),
            asJSON("2163-09-15", 5, "schedule_test",         2, false),
            asJSON("2063-03-17", 3, "start_test",            1, false),
            asJSON("9999-12-31", 0, "t_create_test",         3, false)])
        .toss();

    frisby.create("enter a user")
        .post(API + tourn_1 + "/register/" + player_1, {},
            {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(player_1))
        .expectStatus(200)
        .expectBodyContains("Application Submitted")
        .after(function(){
            frisby.create("check they are entered")
                .get(API + tourn_1 + "/entry/")
                .expectStatus(200)
                .expectJSON([player_1])
                .toss();
        })
        .toss();

    frisby.create("enter a user a second time")
        .post(API + tourn_1 + "/register/" + player_1, {},
            {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(player_1))
        .expectStatus(400)
        .expectBodyContains("You've already applied to " + tourn_1)
        .toss();

    frisby.create("enter a user as someone else")
        .post(API + tourn_1 + "/register/" + player_2, {},
            {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth(player_1))
        .expectStatus(403)
        .expectBodyContains("Permission denied")
        .toss();

    frisby.create("enter user as superuser")
        .post(API + tourn_1 + "/register/" + player_2)
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(200)
        .expectBodyContains("Application Submitted")
        .after(function(){
            frisby.create("check they are entered")
                .get(API + tourn_1 + "/entry/", {inspectOnFailure: true})
                .expectStatus(200)
                .expectJSON(
                    [player_1, player_2])
                .toss();
        })
        .toss();

    frisby.create("enter a non-user")
        .post(API + tourn_1 + "/register/noone", {}, {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(400)
        .expectBodyContains("Check username and tournament")
        .toss();

    frisby.create("malformed")
        .post(API + tourn_1 + "/register", {}, {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(404)
        .toss();

    frisby.create("a non-existent tournament")
        .post(API + "foo/register/" + player_1, {}, {inspectOnFailure: true})
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(400)
        .expectBodyContains("Tournament foo not found in database")
        .toss();
});
