var frisby = require("frisby"),
    utils = require("./utils");

describe("Check auth for page", function () {
    "use strict";
    frisby.create("Visit page with no auth")
        .get(process.env.API_ADDR + "tournament/ranking_test/entry/ranking_test_player_4/enterscore")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();

    frisby.create("Content with no auth")
        .get(process.env.API_ADDR + "tournament/ranking_test/entry/ranking_test_player_4/enterscore/content")
        .expectStatus(200)
        .expectJSON({
            error: "Could not verify your access level for that URL.\nYou have to login with proper credentials"
            })
        .toss();
});

describe("Bad targets", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/painting_test/entry/";
    utils.asUser("superman", "password", function(cookie) {
        frisby.create("Non-user")
            .get(API + "james_rick/enterscore/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                error: "Unknown player: james_rick"
                })
            .toss();
        });

    utils.asUser("superman", "password", function(cookie) {
        frisby.create("User not found")
            .get(API + "ranking_test_player_3/enterscore/content")
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                error: "Entry for ranking_test_player_3 in tournament " +
                    "painting_test not found"
                })
            .toss();
        });
});

describe("Enter some scores", function () {
    "use strict";
    var API = process.env.API_ADDR + "tournament/painting_test/" +
            "entry/rick_james/enterscore",
        badValues = function(user, pass, postData, name, msg) {

            utils.asUser(user, pass, function(cookie) {
                frisby.create(name)
                    .post(API, postData)
                    .addHeader("cookie", cookie)
                    .expectStatus(400)
                    .expectJSON({error: msg})
                    .toss();
                });
            };

    badValues("charlie_murphy", "password",
        {key: "Fanciness", value: 3},
        "Other user",
        "Permission denied for charlie_murphy to perform enter_score on tournament painting_test");

    badValues("rick_james", "password",
        {key: "Fanciness", value: 3},
        "Invalid score",
        "Invalid score: 3");

    badValues("rick_james", "password",
        {key: "Fanciness", value: 16},
        "Invalid score",
        "Invalid score: 16");

    utils.asUser("rick_james", "password", function(cookie) {
        var scoreInfo = {
            key: "Fanciness",
            value: 5};

        frisby.create("Enter good score")
            .post(API, scoreInfo)
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .expectJSON({
                message: "Score entered for rick_james: 5"
                })
            .toss();
        });

    badValues("rick_james", "password",
        {key: "Fanciness", value: 6},
        "Enter score twice",
        "6 not entered. Score is already set");
});
