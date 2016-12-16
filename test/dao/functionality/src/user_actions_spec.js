describe("Enter score for single game for an entry", function () {
    "use strict";
    var frisby = require("frisby"),
        API = process.env.API_ADDR + "user/";

    frisby.create("get actions for a player")
        .get(API + "rank_test_player_1/actions", {inspectOnFailure: true})
        .addHeader("Authorization", "Basic " + new Buffer(
            "rank_test_player_1:password").toString("base64"))
        .expectStatus(200)
        .expectJSONTypes(Array)
        .expectJSONTypes("*", {
            actions: Array,
            title: String
        })
        .expectJSONTypes("0.actions.*", {
            text: String,
            action: String
        })
        .expectJSON("0.actions.0", {
            text: "See upcoming tournaments",
            action: "tournament_list"
        })
        .expectJSON("1.actions.?", {
            text: "Update your details",
            action: "user_update",
            username: "rank_test_player_1"
        })
        .toss();
});
