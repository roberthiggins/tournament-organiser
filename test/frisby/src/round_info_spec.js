var frisby = require("frisby"),
    API = process.env.API_ADDR,
    auth = function(user, pass){
        return "Basic " + new Buffer(user + ":" + pass).toString("base64");
    },
    injector = require("./data_injector"),
    tournament = "round_test";

injector.createTournament("round_test", "2095-07-07");

describe("Set Rounds normally", function () {
    "use strict";
    injector.postRounds(tournament, 2);
    injector.setMissions(tournament, ["mission_1", "mission_2"]);
    frisby.create("Check those missions exist")
        .get(API + "tournament/round_test/rounds/1")
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: "mission_1"
        })
        .toss();
    frisby.create("Check those missions exist")
        .get(API + "tournament/round_test/rounds/2")
        .expectStatus(200)
        .expectJSONTypes({
            draw: Array,
            mission: String
        })
        .expectJSON({
            draw: Array,
            mission: "mission_2"
        })
        .toss();
});

describe("Set Rounds auth", function () {
    "use strict";

    frisby.create("TO auth")
        .post(API + "tournament/round_test/rounds", {
            numRounds: 2
        }, {json: true})
        .addHeader("Authorization", auth("round_test_to", "password"))
        .expectStatus(200)
        .toss();
    frisby.create("No auth")
        .post(API + "tournament/round_test/rounds", {
            numRounds: 2
        }, {json: true})
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
    frisby.create("Bad auth")
        .post(API + "tournament/round_test/rounds", {
            numRounds: 2
        }, {json: true})
        .addHeader("Authorization", auth("enter_score_entry_1", "password"))
        .expectStatus(401)
        .expectBodyContains("Could not verify your access level")
        .toss();
});

describe("Set malformed rounds", function () {
    "use strict";

    var malformedRounds = function(msg, tourn, path, code){
        frisby.create("GET incorrect rounds: " + msg)
            .get(API + "tournament/" + tourn + "/rounds/" + path)
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
