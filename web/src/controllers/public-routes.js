// Publicly available routes
var express = require('express'),
    router  = express.Router(),
    users   = require("./users");


// Home
router.route("/")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/index.js"});
    });

// User mgmt
router.route("/login")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/login.js"});
    })
    .post(users.login);
router.route("/signup")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/signup.js"});
    })
    .post(users.signup);


module.exports = router;
