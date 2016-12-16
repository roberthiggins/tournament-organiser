var frisby = require("frisby"),
    tournament = "round_test",
    API = process.env.API_ADDR + "tournament/" + tournament,
    injector = require("./data_injector");

injector.createTournament("round_test", "2095-07-07", 2, ["miss_1", "miss_2"]);

describe("Set Rounds normally", function () {
    "use strict";
    frisby.create("Check those missions exist")
        .get(API + "/rounds/1")
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: "miss_1"
        })
        .toss();
    frisby.create("Check those missions exist")
        .get(API + "/rounds/2")
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: "miss_2"
        })
        .toss();
});

describe("Set Rounds auth", function () {
    "use strict";

    frisby.create("TO auth")
        .post(API, {
            rounds: 2
        }, {json: true})
        .addHeader("Authorization", injector.auth("round_test_to"))
        .expectStatus(200)
        .toss();
    frisby.create("No auth")
        .post(API, {
            rounds: 2
        }, {json: true})
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
    frisby.create("Bad auth")
        .post(API, {
            rounds: 2
        }, {json: true})
        .addHeader("Authorization", injector.auth("enter_score_entry_1"))
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
});

describe("Set malformed rounds", function () {
    "use strict";

    var malformedRounds = function(msg, trn, pth, code){
        frisby.create("GET incorrect rounds: " + msg)
            .get(process.env.API_ADDR + "tournament/" + trn + "/rounds/" + pth)
            .expectStatus(code)
            .toss();
    };

    malformedRounds("fake tourn", "foo", 1, 400);
    malformedRounds("big round", "round_test", 4, 400);
    malformedRounds("negative rd", "round_test", -1, 400);
    malformedRounds("character", "round_test", "a", 400);
    malformedRounds("transpose", 1, "round_test", 400);
    malformedRounds("extra path", "round_test", "1/1", 404);
});
