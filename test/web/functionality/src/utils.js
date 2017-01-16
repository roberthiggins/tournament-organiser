var frisby = require("frisby");

exports.asUser = function (user, pword, afterFunc) {
    frisby.create("Login")
        .post(process.env.API_ADDR + "login", {
            username: user,
            password: pword
            })
        .expectStatus(200)
        .after(function(err, res, body) {
            afterFunc(res.headers["set-cookie"][0], err, res, body);
            })
        .toss();
};
