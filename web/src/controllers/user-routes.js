// Only members can see these routes

var DAOAmbassador  = require("../lib/dao-ambassador"),
    express        = require('express'),
    router         = express.Router(),
    users          = require("../lib/users"),
    injectAuthUser = [users.injectUserIntoRequest, users.ensureAuthenticated];

router.route("/user/:user")
    .get(injectAuthUser, function(req, res) {
        res.render("basic", {
            src_loc: "/userDetails.js",
            subtitle: "User Details for " + req.user.username
        });
    });
router.route("/user/:user/content")
    .get(injectAuthUser, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/user/" + req.params.user,
            onSuccess: function(resp) {
                res.status(200).json({user: JSON.parse(resp)});
                }
            });
        });

router.route("/user/:user/update")
    .get(injectAuthUser, function(req, res) {
        res.render("basic", {
            src_loc: "/userUpdate.js",
            subtitle: "Update user details for " + req.user.username
        });
        })
    .post(injectAuthUser, function(req, res) {
        DAOAmbassador.request({
            method: "PUT",
            request: req,
            response: res,
            URL: "/user/" + req.params.user,
            data: req.body,
            });
        });
router.route("/user/:user/update/content")
    .get(injectAuthUser, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/user/" + req.params.user,
            onSuccess: function(resp) {
                res.status(200).json({user: JSON.parse(resp)});
                }
            });
        });

module.exports = router;
