var frisby = require("frisby"),
    injector = require("./data_injector"),
    tournament = "mission_test",
    p1 = "mission_test_player_1",
    API = process.env.API_ADDR;

(function setup() {
    injector.createTournament(tournament, "2095-07-01", 3,
        ["Mission the First", "Missions the Second", "Mission the Third"]);
    injector.createUser(p1);
    injector.enterTournament(tournament, p1);
})();

describe("Normal behaviour", function () {
    "use strict";

    // Normal behaviour
    injector.postRounds(tournament, 3);
    injector.setMissions(tournament, ["mission_1", "mission_2", "mission_3"]);
    frisby.create("Check those missions exist")
        .get(API + "tournament/mission_test/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "mission_3"])
        .toss();

    // set missions and then change number of rounds
    injector.postRounds(tournament, 4);
    frisby.create("Check 4th round is TBA")
        .get(API + "tournament/mission_test/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "mission_3", "TBA"])
        .toss();
    injector.postRounds(tournament, 2);
    injector.postRounds(tournament, 3);
    frisby.create("Check 3rd round is TBA and 4th is gone")
        .get(API + "tournament/mission_test/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "TBA"])
        .toss();
});

describe("Missions Auth", function () {
    "use strict";

    var authTestMissions = function(msg, user, code){
            frisby.create("POST missions as: " + msg)
                .post(API + "tournament/mission_test/missions", {
                    missions: ["mission_1", "mission_2", "mission_3"]
                }, {json: true})
                .addHeader("Authorization", "Basic " +
                    new Buffer(user + ":password").toString("base64"))
                .expectStatus(code)
                .toss();
        };
    authTestMissions("TO", "mission_test_to", 200);
    authTestMissions("Player", p1, 403);
    authTestMissions("Super", "superuser", 200);
    authTestMissions("Other user", "rank_test_player_1", 403);
    authTestMissions("Non-user", "rfdsfsdfk_test_player_1", 401);
    frisby.create("POST missions with no auth")
        .post(API + "tournament/mission_test/missions", {
            missions: ["mission_1", "mission_2", "mission_3"]
        }, {json: true})
        .expectStatus(401)
        .toss();
});

describe("Malformed Missions", function () {
    "use strict";

    var postMalformedMissions = function(msg, tourn, postData){
        frisby.create("POST malformed missions: " + msg)
            .post(API + "tournament/" + tourn + "/missions", {
                missions: postData
            }, {json: true})
            .addHeader("Authorization", "Basic " +
                new Buffer("superuser:password").toString("base64"))
            .expectStatus(400)
            .toss();
    };
    postMalformedMissions("fake tourn", "not_real", ["m_1", "m_2", "m_3"]);
    postMalformedMissions("dict", "mission_test", {});
    postMalformedMissions("too few", "mission_test", ["m_1", "m_2"]);
    postMalformedMissions("too many", "mission_test", ["1", "2", "3", "4"]);
    postMalformedMissions("none", "mission_test", []);
});
