var frisby = require("frisby"),
    injector = require("./data_injector"),
    API = process.env.API_ADDR;


describe("Signing up and seeing user details", function () {
    "use strict";

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
                .addHeader("Authorization", injector.auth("superuser"))
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
                .addHeader("Authorization", injector.auth("superuser"))
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
});

describe("User Accounts - unhappy path", function () {
    "use strict";

    frisby.create("Malformed")
        .get(API + "user/")
        .addHeader("Authorization", injector.auth("superuser"))
        .expectStatus(404)
        .toss();

    frisby.create("Look for a user who doesn't exist")
        .get(API + "user/jim_bob_noname")
        .addHeader("Authorization", injector.auth("superuser"))
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
        .addHeader("Authorization", injector.auth("noone"))
        .expectStatus(401)
        .toss();
});

describe("Updating an existing user", function () {
    "use strict";
    var user = "modify_user",
        api = API + "user/" + user;

    frisby.create("Happy path update")
        .post(api, {
            email: user + "@foobar.com",
            password1: "foo",
            password2: "foo",
            first_name: "Name1",
            last_name: "Name2",
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .after(function(){
            frisby.create("Modify the user details")
                .put(api, {
                    email: user + "@foobar.com",
                    first_name: "FirstName",
                    last_name: "LastName",
                    }, {json: true, inspectOnFailure: true})
                .addHeader("Authorization", injector.auth(user, "foo"))
                .expectStatus(200)
                .after(function() {
                    frisby.create("Details should have been updated")
                        .get(api)
                        .addHeader("Authorization", injector.auth(user, "foo"))
                        .expectStatus(200)
                        .expectJSON({
                            username: user,
                            email: user + "@foobar.com",
                            first_name: "FirstName",
                            last_name: "LastName"
                            })
                        .toss();
                    })
                .toss();
        })
        .toss();


    var user2 = "modify_user_2",
        api2 = API + "user/" + user2;
    frisby.create("Another user attempts to update you")
        .post(api2, {
            email: user + "@foobar.com",
            password1: "password",
            password2: "password",
            first_name: "Name1",
            last_name: "Name2",
        }, {json: true, inspectOnFailure: true})
        .expectStatus(200)
        .after(function(){
            frisby.create("Modify the user details")
                .put(api2, {
                    email: user + "@foobar.com",
                    first_name: "FirstName",
                    last_name: "LastName",
                    }, {json: true, inspectOnFailure: true})
                .addHeader("Authorization", injector.auth(user))
                .expectStatus(401)
                .toss();
        })
        .toss();
});
