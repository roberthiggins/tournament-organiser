describe("Get info about tournament entries", function () {
    "use strict";
    var frisby = require("frisby"),
        injector = require("./data_injector"),
        tourn = "entry_info_test",
        entry = "entry_info_test_player",
        API = process.env.API_ADDR + "tournament/" + tourn + "/entry/";

    injector.createTournament(tourn, "2095-07-02", null, null, null, [entry]);

    frisby.create("Info about an entry")
        .get(API + entry)
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes(
            {
                username: String,
                tournament_name: String,
                entry_id: Number
            }
        )
        .expectJSON(
            {
                username: entry,
                tournament_name: tourn,
            }
        )
        .toss();

    frisby.create("A non-existent user")
        .get(API + "flubber")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(400)
        .expectHeaderContains("content-type", "text/html")
        .expectBodyContains("Unknown player: flubber")
        .toss();
    frisby.create("malformed")
        .get(API + "entry_info_test_player/a")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(404)
        .toss();

    // permissions
    frisby.create("Info about an entry as random user")
        .get(API + entry)
        .addHeader("Authorization", "Basic " +
            new Buffer("rank_test_player_1:password").toString("base64"))
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes(
            {
                username: String,
                tournament_name: String,
                entry_id: Number
            }
        )
        .expectJSON(
            {
                username: entry,
                tournament_name: tourn,
            }
        )
        .toss();
    frisby.create("Info about an entry with no auth")
        .get(API + entry)
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
    frisby.create("Info about an entry with non-existent user")
        .get(API + entry)
        .addHeader("Authorization", "Basic " +
            new Buffer("superusersuperuser:password").toString("base64"))
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
});
