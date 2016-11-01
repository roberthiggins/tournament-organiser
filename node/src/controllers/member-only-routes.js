// Only members can see these routes

var DAOAmbassador = require("../lib/dao-ambassador"),
    express       = require('express'),
    feedback      = require("./feedback"),
    router        = express.Router(),
    users         = require("./users");

var injectAuthUser = [users.injectUserIntoRequest, users.ensureAuthenticated];

router.route("/devindex")
    .get(injectAuthUser, function(req, res) {
        res.render("basic", {src_loc: "/devindex.js"});
    });
router.route("/devindex/content")
    .get(injectAuthUser, function(req, res) {
        var url = "/user/" + req.user.username + "/actions";

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(body) {
                var transformer = require("../models/menu");
                res.status(200).json(transformer.transform(JSON.parse(body)));
            });
    });

router.route("/feedback")
    .get(injectAuthUser, function(req, res) {
        res.render("basic", {
            src_loc: "/feedback.js",
            subtitle: "Place Feedback"
        });
    })
    .post(injectAuthUser, feedback.placeFeedback);

router.route("/logout")
    .get(injectAuthUser, users.logout);

router.route("/user/:user")
    .get(injectAuthUser, function(req, res) {
        res.render("basic", {
            src_loc: "/userDetails.js",
            subtitle: "User Details for " + req.user.username
        });
    })
router.route("/user/:user/content")
    .get(injectAuthUser, function(req, res) {
        DAOAmbassador.getFromDAORequest(
            req,
            res,
            "/user/" + req.params.user,
            function(resp) {
                res.status(200).json({user: JSON.parse(resp)});
            });
    })

module.exports = router;
