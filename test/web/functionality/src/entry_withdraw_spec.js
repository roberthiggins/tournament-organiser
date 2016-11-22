var frisby = require("frisby"),
    utils = require("./utils"),
    tourn = "withdrawal_test",
    API = process.env.API_ADDR + "tournament/" + tourn + "/entry/",
    p1 = tourn + "_p_1",
    p2 = tourn + "_p_2";


describe("Auth", function () {
    "use strict";
    frisby.create("no auth")
        .post(API + p1 + "/withdraw", {}, {inspectOnFailure: true})
        .expectStatus(302)
        .expectBodyContains("/login?")
        .toss();

    utils.asUser(p2, "password", function(cookie){
        frisby.create("another player")
            .post(API + p1 + "/withdraw", {}, {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(400)
            .expectJSON({error: "Permission denied for " + p2 +
                " to perform modify_application on tournament " + tourn})
            .toss();
    });
});

describe("Withdraw", function () {
    "use strict";
    utils.asUser(p1, "password", function(cookie){
        frisby.create("withdraw as player")
            .post(API + p1 + "/withdraw", {}, {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .toss();
    });

    utils.asUser("superman", "password", function(cookie){
        frisby.create("withdraw as TO")
            .post(API + p2 + "/withdraw", {}, {inspectOnFailure: true})
            .addHeader("cookie", cookie)
            .expectStatus(200)
            .toss();
    });
});
