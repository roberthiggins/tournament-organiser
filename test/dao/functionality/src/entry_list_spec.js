describe("Get a list of entries from a tournament", function () {
    "use strict";
    var frisby = require("frisby"),
        injector = require("./data_injector"),
        API = process.env.API_ADDR;

    injector.createTournament("entry_list_test", '2095-07-03', null, null, null,
        ["entry_list_test_player_1", "entry_list_test_player_2"]);
    injector.createTournament("entry_list_test_empty", '2095-07-04');

    frisby.create("Details for existing tournament")
        .get(API + "tournament/entry_list_test/entry/")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSONTypes("*", String)
        .expectJSON([
            "entry_list_test_player_1",
            "entry_list_test_player_2"
        ])
        .toss();

    frisby.create("Tournament with no entries")
        .get(API + "tournament/entry_list_test_empty/entry/")
        .expectStatus(200)
        .expectHeaderContains("content-type", "application/json")
        .expectJSON([])
        .toss();

    frisby.create("Tournament that does not exist")
        .get(API + "tournament/kdjflskdjflkdjflkdjf/entry/")
        .expectStatus(400)
        .toss();
});
