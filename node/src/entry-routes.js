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
    .get(function(req, res) {
       res.render("basic", {
            src_loc: "/entry.js",
            subtitle: "Entries for " + req.params.tournament
        });
    });
router.route("/tournament/:tournament/entries/content")
    .get(function(req, res) {
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
router.route("/tournament/:tournament/entry/:username/enterscore/content")
    .get(users.injectUserIntoRequest, ensureEntryExists, function(req, res) {
        var url = "/tournament/" + req.params.tournament
            + "/score_categories"

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(responseBody) {
                var responseDict = {
                    categories: JSON.parse(responseBody),
                    message: "Enter score for " + req.params.username,
                };
                res.status(200).json(responseDict);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
            });
    });


module.exports = router;
