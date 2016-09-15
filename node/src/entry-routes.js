// Tournament information
var DAOAmbassador = require("./dao-ambassador"),
    express       = require('express'),
    router        = express.Router(),
    users         = require("./users");


var ensureEntryExists = function(req, res, next) {
    var url = "/tournament/" + req.params.tournament + "/entry/"
        + req.params.username;

    DAOAmbassador.getFromDAORequest(req, res, url,
        function success() {
            next();
        },
        function failure(responseBody){
            res.status(200).json({error: responseBody});
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
        var url = "/tournament/" + req.params.tournament + "/entry/";

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(responseBody) {
                var responseDict = {
                    entries: JSON.parse(responseBody),
                    tournament : req.params.tournament
                };
                res.status(200).json(responseDict);
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
                scorer:  req.user.username,
                value:   req.body.value,
                game_id: req.body.gameId
            };
        DAOAmbassador.postToDAORequest(req, res, url, postData,
            undefined,
            function(responseBody) {
                res.status(400).json({error: responseBody});
            });
        });
router.route("/tournament/:tournament/entry/:username/entergamescore/scorecategories")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament
            + "/score_categories";

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                res.status(200).json({categories: JSON.parse(responseBody)});
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
            });
    })
router.route("/tournament/:tournament/entry/:username/entergamescore/content")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/entry/"
            + req.params.username + "/nextgame";

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                var response = JSON.parse(responseBody);
                response.message = "Enter score for " + req.params.tournament
                    + ", Round " + response.round;
                response.perTournament = false;
                res.status(200).json(response);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
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
                scorer: req.user.username,
                value:  req.body.value
            };
        DAOAmbassador.postToDAORequest(req, res, url, postData,
            undefined,
            function(responseBody) {
                res.status(400).json({error: responseBody});
            });
        });
router.route("/tournament/:tournament/entry/:username/enterscore/scorecategories")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament
            + "/score_categories";

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                res.status(200).json({categories: JSON.parse(responseBody)});
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
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
        var url = "/tournament/" + req.params.tournament + "/entry/"
            + req.params.username + "/nextgame";

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                res.status(200).json({
                    message: "Next Game Info for " + req.params.username,
                    nextgame: JSON.parse(responseBody)
                });
            },
            function(responseBody) {
                res.status(200).json({
                    message: responseBody,
                    nextgame: null
                });
            });
    });

module.exports = router;
