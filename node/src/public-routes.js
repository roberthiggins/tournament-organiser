// Publicly available routes
var dao     = require("./dao-ambassador"),
    express = require('express'),
    router  = express.Router(),
    users   = require("./users");


// Home
router.route("/")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/devindex.js"});
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


// Tournaments
router.route("/tournaments")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/tournamentList.js"});
    });
router.route("/tournaments/content")
    .get(function(req, res) {

        dao.getFromDAORequest(req, res, "/tournament/", function(result) {
            res.send(result);
        });
    });

module.exports = router;
