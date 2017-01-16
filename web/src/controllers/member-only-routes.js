// Only members can see these routes

var express        = require('express'),
    feedback       = require("./feedback"),
    router         = express.Router(),
    users          = require("../lib/users"),
    injectAuthUser = [users.injectUserIntoRequest, users.ensureAuthenticated];

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

module.exports = router;
