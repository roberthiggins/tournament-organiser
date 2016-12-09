// Tournament information
var DAOAmbassador = require("../lib/dao-ambassador"),
    express       = require('express'),
    router        = express.Router(),
    users         = require("../lib/users");


var ensureEntryExists = function(req, res, next) {
    DAOAmbassador.request({
        method: "GET",
        request: req,
        response: res,
        URL: "/tournament/" + req.params.tournament + "/entry/"
            + req.params.username,
        onSuccess: function() { next(); },
        onFail: function failure(responseBody){
            res.status(200).json({error: responseBody});
            }
        });
};

var needsUser = [
    users.injectUserIntoRequest,
    users.ensureAuthenticated
];

router.route("/tournament/:tournament/entries")
    .get(needsUser, function(req, res) {
       res.render("basic", {
            src_loc: "/entry.js",
            subtitle: "Entries for " + req.params.tournament
        });
    });
router.route("/tournament/:tournament/entries/content")
    .get(needsUser, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/entry/",
            onSuccess: function(responseBody) {
                var responseDict = {
                    entries: JSON.parse(responseBody),
                    tournament : req.params.tournament
                };
                res.status(200).json(responseDict);
                }
            });
    });

router.route("/tournament/:tournament/entry/:username/entergamescore")
    .get(needsUser, function(req, res) {
        res.render("basic", {
            src_loc: "/entryScore.js",
            subtitle: "Enter score for " + req.params.username
        });
    })
    .post(needsUser, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/entry/"
            + req.params.username + "/entergamescore",
            postData = {
                key:     req.body.key,
                value:   req.body.value,
                game_id: req.body.gameId
            };
        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: url,
            data: postData,
            });
        });
router.route("/tournament/:tournament/entry/:username/entergamescore/scorecategories")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/score_categories",
            onSuccess: function(responseBody) {
                res.status(200).json({categories: JSON.parse(responseBody)});
                },
            onFail: function(responseBody) {
                res.status(200).json({error: responseBody});
                }
            });
    })
router.route("/tournament/:tournament/entry/:username/entergamescore/content")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/entry/"
                + req.params.username + "/nextgame",
            onSuccess: function(responseBody) {
                var response = JSON.parse(responseBody);
                response.message = "Enter score for " + req.params.tournament
                    + ", Round " + response.round;
                response.perTournament = false;
                res.status(200).json(response);
                },
            onFail: function(responseBody) {
                res.status(200).json({error: responseBody});
                }
            });
    });

router.route("/tournament/:tournament/entry/:username/enterscore")
    .get(needsUser, function(req, res) {
        res.render("basic", {
            src_loc: "/entryScore.js",
            subtitle: "Enter score for " + req.params.username
        });
    })
    .post(needsUser, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/entry/"
            + req.params.username + "/entertournamentscore",
            postData = {
                key:    req.body.key,
                value:  req.body.value
            };
        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: url,
            data: postData
            });
        });
router.route("/tournament/:tournament/entry/:username/enterscore/scorecategories")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL:  "/tournament/" + req.params.tournament + "/score_categories",
            onSuccess: function(responseBody) {
                res.status(200).json({categories: JSON.parse(responseBody)});
            },
            onFail: function(responseBody) {
                res.status(200).json({error: responseBody});
                }
            });
    })
router.route("/tournament/:tournament/entry/:username/enterscore/content")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        res.status(200).json({
            message: "Enter score for " + req.params.username,
            perTournament : true
        });
    });

router.route("/tournament/:tournament/entry/:username/nextgame")
    .get(needsUser, function(req, res) {
        res.render("basic", {
            src_loc: "/entryNextGame.js",
            subtitle: "Next Game Information for " + req.params.username
        });
    });
router.route("/tournament/:tournament/entry/:username/nextgame/content")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/entry/"
                    + req.params.username + "/nextgame",
            onSuccess: function(responseBody) {
                res.status(200).json({
                    message: "Next Game Info for " + req.params.username,
                    nextgame: JSON.parse(responseBody)
                });
                },
            onFail: function(responseBody) {
                res.status(200).json({
                    message: responseBody,
                    nextgame: null
                    });
                }
            });
    });

router.route("/tournament/:tournament/entry/:username/withdraw")
    .post(needsUser, ensureEntryExists, function(req, res) {
        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/entry/"
                + req.params.username + "/withdraw"
            });
        });

module.exports = router;
