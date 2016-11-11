describe("Signing up and seeing user details", function () {
    "use strict";
    var frisby = require("frisby"),
        API = process.env.API_ADDR;

    frisby.create("See user details")
        .post(API + "user/sign_up_user", {
            email: "sign_up_user@foobar.com",
            password1: "foo",
            password2: "foo",
            first_name: "Herpity",
            last_name: "Derp",
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .after(function(){
            frisby.create("See user details")
                .get(API + "user/sign_up_user")
                .addHeader("Authorization", "Basic " +
                    new Buffer("superuser:password").toString("base64"))
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSONTypes({
                    username: String,
                    email: String,
                    first_name: String,
                    last_name: String,
                   })
                .expectJSON({
                    username: "sign_up_user",
                    email: "sign_up_user@foobar.com",
                    first_name: "Herpity",
                    last_name: "Derp",
                    })
                .toss();
        })
        .toss();

    frisby.create("See user details no first/last name")
        .post(API + "user/capt_no_name", {
            email: "capt_no_name@foobar.com",
            password1: "foo",
            password2: "foo",
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .after(function(){
            frisby.create("See user details")
                .get(API + "user/capt_no_name")
                .addHeader("Authorization", "Basic " +
                    new Buffer("superuser:password").toString("base64"))
                .expectStatus(200)
                .expectHeaderContains("content-type", "application/json")
                .expectJSONTypes({
                    username: String,
                    email: String,
                    first_name: String,
                    last_name: String,
                    })
                .expectJSON({
                    username: "capt_no_name",
                    email: "capt_no_name@foobar.com",
                    first_name: "",
                    last_name: "",
                    })
                .toss();
        })
        .toss();


    frisby.create("Malformed")
        .get(API + "user/")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(404)
        .toss();

    frisby.create("Look for a user who doesn't exist")
        .get(API + "user/jim_bob_noname")
        .addHeader("Authorization", "Basic " +
            new Buffer("superuser:password").toString("base64"))
        .expectStatus(400)
        .expectHeaderContains("content-type", "text/html")
        .expectBodyContains("Cannot find user jim_bob_noname")
        .toss();

    frisby.create("See user details with no auth")
        .get(API + "user/charlie_murphy")
        .expectStatus(401)
        .toss();

    frisby.create("See user details with bad auth")
        .get(API + "user/charlie_murphy")
        .addHeader("Authorization", "Basic " +
            new Buffer("noone:password").toString("base64"))
        .expectStatus(401)
        .toss();
});
