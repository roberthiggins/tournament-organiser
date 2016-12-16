var frisby = require("frisby"),
    injector = require("./data_injector");

var tournAPI = function(tourn) {
        return process.env.API_ADDR + "tournament/" + tourn;
    },
    checkEntries = function(tourn, entryCount) {
        frisby.create("check number of entries is " + entryCount)
            .get(tournAPI(tourn), {inspectOnFailure: true})
            .expectStatus(200)
            .expectJSON({
                name: tourn,
                entries: entryCount,
                date: "3121-03-18",
                score_categories: [],
                rounds: 0
                })
            .toss();
    },
    success = function(tourn){
        return "Entry to " + tourn + " withdrawn successfully";
    },
    setup = function(tourn, entries) {
        injector.createTournament(tourn, "3121-03-18", null, null, null,
            entries);
    };

describe("Test withdrawing tournament", function () {
    "use strict";

    var tourn = "withdrawal_test",
        entry = tourn + "_p1",
        withdrawAPI = tournAPI(tourn) + "/entry/" + entry + "/withdraw";

    setup(tourn, [entry]);

    frisby.create("Withdraw from a tournament")
        .post(withdrawAPI)
        .expectStatus(200)
        .addHeader("Authorization", injector.auth(entry))
        .expectBodyContains(success(tourn))
        .after(function() {
            checkEntries(tourn, 0);
            })
        .toss();

    frisby.create("Withdraw from a tournament twice")
        .post(withdrawAPI)
        .addHeader("Authorization", injector.auth(tourn + "_to"))
        .expectStatus(400)
        .expectBodyContains("Entry for " + entry + " in tournament " +
            tourn + " not found")
        .after(function() {
            checkEntries(tourn, 0);
            })
        .toss();
});

describe("Test re-applying", function () {
    "use strict";

    var tourn = "withdrawal_test_2",
        entry = tourn + "_p_1",
        withdrawAPI = tournAPI(tourn) + "/entry/" + entry + "/withdraw";

    setup(tourn, [entry]);

    frisby.create("First withdraw from tournament")
        .post(withdrawAPI)
        .addHeader("Authorization", injector.auth(entry))
        .expectStatus(200)
        .after(function() {
            frisby.create("Then re-apply")
                .post(tournAPI(tourn) + "/register/" + entry, {},
                    {inspectOnFailure: true})
                .addHeader("Authorization", injector.auth(entry))
                .expectStatus(200)
                .toss();
            })
        .toss();
});

describe("Test withdrawing tournament with Auth problems", function () {
    "use strict";

    var tourn = "withdrawal_test_3",
        entry1 = tourn + "_p1",
        entry2 = tourn + "_p2",
        withdrawAPI = tournAPI(tourn) + "/entry/" + entry1 + "/withdraw";

    setup(tourn, [entry1, entry2]);

    frisby.create("Withdraw from a tournament - no auth")
        .post(withdrawAPI)
        .expectStatus(401)
        .after(function() {
            checkEntries(tourn, 2);
        })
        .toss();

    frisby.create("Withdraw from a tournament - wrong auth")
        .post(withdrawAPI)
        .addHeader("Authorization", injector.auth("rank_test_player_1"))
        .expectStatus(403)
        .expectBodyContains("Permission denied")
        .after(function() {
            checkEntries(tourn, 2);
        })
        .toss();
});
