var frisby = require("frisby"),
    injector = require("./data_injector"),
    tournament = "mission_test",
    p1 = "mission_test_player_1",
    API = process.env.API_ADDR + "tournament/" + tournament;

(function setup() {
    injector.createTournament(tournament, "2095-07-01", 3,
        ["mission_1", "mission_2", "mission_3"], null, [p1]);
    injector.createTournament("empty_tournament", "2095-07-01");
})();

describe("Getting missions when rounds have not been set", function(){
    "use strict";
    frisby.create("No rounds set should throw an error")
        .get(process.env.API_ADDR + "tournament/empty_tournament/missions")
        .expectStatus(400)
        .expectBodyContains("Please set the number of rounds for empty_tournament first")
        .toss();
});

describe("Normal behaviour", function () {
    "use strict";

    // Normal behaviour
    frisby.create("Check those missions exist")
        .get(API + "/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "mission_3"])
        .toss();

    // set missions and then change number of rounds
    injector.postRounds(tournament, 4);
    frisby.create("Check 4th round is TBA")
        .get(API + "/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "mission_3", "TBA"])
        .toss();
    injector.postRounds(tournament, 2);
    injector.postRounds(tournament, 3);
    frisby.create("Check 3rd round is TBA and 4th is gone")
        .get(API + "/missions")
        .expectStatus(200)
        .expectJSONTypes("*", Array)
        .expectJSON(["mission_1", "mission_2", "TBA"])
        .toss();
});

describe("Missions Auth", function () {
    "use strict";

    var authTestMissions = function(msg, user, code){
            frisby.create("POST missions as: " + msg)
                .post(API, {
                    missions: ["mission_1", "mission_2", "mission_3"]
                }, {json: true})
                .addHeader("Authorization", injector.auth(user))
                .expectStatus(code)
                .toss();
        };
    authTestMissions("TO", "mission_test_to", 200);
    authTestMissions("Player", p1, 403);
    authTestMissions("Super", "superuser", 200);
    authTestMissions("Other user", "rank_test_player_1", 403);
    authTestMissions("Non-user", "rfdsfsdfk_test_player_1", 401);
    frisby.create("POST missions with no auth")
        .post(API, {
            missions: ["mission_1", "mission_2", "mission_3"]
        }, {json: true})
        .expectStatus(401)
        .toss();
});

describe("Malformed Missions", function () {
    "use strict";

    var url = process.env.API_ADDR + "tournament/",
        postMalformedMissions = function(msg, tourn, postData, error){
            frisby.create("POST malformed missions: " + msg)
                .post(url + tourn, {missions: postData}, {json: true})
                .addHeader("Authorization", injector.auth("superuser"))
                .expectStatus(400)
                .expectBodyContains(error)
                .toss();
            };
    postMalformedMissions("fake tourn", "not_real", ["m_1", "m_2", "m_3"],
        "Tournament not_real not found in database");
    postMalformedMissions("dict", "mission_test", {},
        "Tournament mission_test has 3 rounds. You submitted missions []");
    postMalformedMissions("none", "mission_test", [],
        "Tournament mission_test has 3 rounds. You submitted missions []");
    postMalformedMissions("too few", "mission_test", ["1", "2"],
        "Tournament mission_test has 3 rounds. You submitted missions " +
        "[\"1\", \"2\"]");
    postMalformedMissions("too many", "mission_test", ["1", "2", "3", "4"],
        "Tournament mission_test has 3 rounds. You submitted missions " +
        "[\"1\", \"2\", \"3\", \"4\"]");
});
