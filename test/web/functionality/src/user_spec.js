var frisby = require("frisby"),
    utils = require("./utils");

describe("Login", function () {
    "use strict";
    frisby.create("Login Page")
        .get(process.env.API_ADDR + "login")
        .expectStatus(200)
        .expectBodyContains("login.js")
        .toss();
});

describe("Login with bad details", function () {
    "use strict";
    var badLogin = function(name, details, msg) {
        frisby.create(name)
            .post(process.env.API_ADDR + "login", details)
            .expectStatus(400)
            .expectJSONTypes({message: String})
            .expectJSON({message: msg})
            .toss();
    };

    badLogin("no uname", {password: "bar"}, "Missing credentials");
    badLogin("no pword", {username: "foo"}, "Missing credentials");
    badLogin("nothing", {}, "Missing credentials");
    badLogin("bad user",
             {username: "steveqmcqueenie", password: "password123"},
             "Username or password incorrect");
    badLogin("bad pass",
             {username: "steveqmcqueen", password: "password12"},
             "Username or password incorrect");
});

describe("Login twice", function () {
    "use strict";
    utils.asUser("superman", "password", function() {
        frisby.create("second login")
            .post(process.env.API_ADDR + "login",
                {username: "charlie_murphy", password: "password"})
            .expectStatus(200)
            .toss();
        });
});

describe("Sign Up Page", function () {
    "use strict";
    frisby.create("Sign Up Page")
        .get(process.env.API_ADDR + "signup")
        .expectStatus(200)
        .expectBodyContains("signup.js")
        .toss();
});

describe("Sign Up Values", function () {
    "use strict";
    var API = process.env.API_ADDR + "signup",
        badValue = function(name, msg, details){
            frisby.create(name)
                .post(API, details)
                .expectStatus(400)
                .expectJSON({error: msg})
                .toss();

            };

    frisby.create("Happy path")
        .post(API, {
            username: "su_test_1",
            email: "a@b.c",
            password1: "password",
            password2: "password"})
        .expectStatus(200)
        .expectJSON({
            message: "<p>Account created! You submitted the following fields" +
                ":</p><ul><li>User Name: su_test_1</li><li>Email: a@b.c</li>" +
                "</ul>"})
        .toss();

    badValue("Already exists",
        "A user with the username su_test_1 already exists! Please choose another name",
        {
            username: "su_test_1",
            email: "a@b.c",
            password1: "password",
            password2: "password"
        });

    badValue("Empty email",
        "This email does not appear valid",
        {
            username: "su_test_2",
            email: "",
            password1: "password",
            password2: "password"
        });
    badValue("No email",
        "Enter the required fields",
        {
            username: "su_test_2",
            password1: "password",
            password2: "password"
        });

    badValue("Empty username",
        "Please enter a username",
        {
            username: "",
            email: "a@b.c",
            password1: "password",
            password2: "password"
        });
    badValue("No username",
        "Please enter a username",
        {
            email: "a@b.c",
            password1: "password",
            password2: "password"
        });


    badValue("Passwords",
        "Please enter two matching passwords",
        {
            username: "su_test_2",
            email: "a@b.c",
            password1: "",
            password2: "password"
        });
    badValue("Passwords",
        "Please enter two matching passwords",
        {
            username: "su_test_2",
            email: "a@b.c",
            password1: "password",
            password2: ""
        });
    badValue("Passwords",
        "Please enter two matching passwords",
        {
            username: "su_test_2",
            email: "a@b.c",
            password1: "",
            password2: ""
        });
    badValue("Passwords",
        "Please enter two matching passwords",
        {
            username: "su_test_2",
            email: "a@b.c",
            password1: "password1",
            password2: "password2"
        });
    badValue("Passwords",
        "Enter the required fields",
        {
            username: "su_test_2",
            email: "a@b.c",
            password2: "password"
        });
    badValue("Passwords",
        "Enter the required fields",
        {
            username: "su_test_2",
            email: "a@b.c",
            password1: "password",
        });
    badValue("Passwords",
        "Enter the required fields",
        {
            username: "su_test_2",
            email: "a@b.c",
        });
});
