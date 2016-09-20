// Publicly available routes
var express = require('express'),
    router  = express.Router(),
    users   = require("./users");


// Home
router.route("/")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/index.js"});
    });
router.route("/devindex")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/devindex.js"});
    });
router.route("/devindex/content")
    .get(function(req, res) {
        var content = require("./models/devindex.js");
        res.send([
            content.enterT,
            content.orgT,
            content.playT,
            content.viewT,
            content.feedback
        ]);
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
