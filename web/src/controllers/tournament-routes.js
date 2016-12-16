// Tournament information
var Category      = require("../models/score-categories"),
    DAOAmbassador = require("../lib/dao-ambassador"),
    express       = require('express'),
    router        = express.Router(),
    users         = require("../lib/users"),
    authUser      = [users.injectUserIntoRequest, users.ensureAuthenticated];


router.route("/tournaments")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/tournamentList.js"});
    });
router.route("/tournaments/content")
    .get(function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/",
            onSuccess: function(result) {
                res.status(200).json(JSON.parse(result));
                }
            });
    });

router.route("/tournament/create")
    .get(authUser, function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentCreate.js",
            subtitle: "Add a Tournament"
            });
        })
    .post(authUser, function(req, res){
        try {
            var cleanCats = Category.cleanCategories(req.body.categories);
            DAOAmbassador.request({
                method: "POST",
                request: req,
                response: res,
                URL: "/tournament",
                data: {
                    inputTournamentName: req.body.name,
                    inputTournamentDate: req.body.date,
                    rounds: req.body.rounds || 0,
                    score_categories: cleanCats
                    },
                onSuccess: function success(result) {
                    res.status(200).json(JSON.parse(result));
                    }
                });
        }
        catch (err) {
            res.status(400).json({error: err});
            return;
        }
        });

router.route("/tournament/:tournament")
    .get(function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentInfo.js",
            subtitle: req.params.tournament
        });
    })
    .post(authUser, function(req, res){
        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament + "/register/" +
                req.user.username,
            });
        });
router.route("/tournament/:tournament/content")
    .get(function(req, res) {
        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament,
            onSuccess: function(result) {
                res.status(200).json(JSON.parse(result));
                },
            });
    });

router.route("/tournament/:tournament/rankings")
    .get(function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentRankings.js",
            subtitle: "Placings for " + req.params.tournament
        });
    })
router.route("/tournament/:tournament/rankings/content")
    .get(function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/entry/rank";

        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: url,
            onSuccess: function(responseBody) {
                var responseDict = {entries: JSON.parse(responseBody)};
                responseDict.tournament = req.params.tournament,

                res.status(200).json(responseDict);
                },
            onFail: function(responseBody) {
                res.status(200).json({error: responseBody});
                }
            });
    });

router.route("/tournament/:tournament/rounds")
    .get(authUser, function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentRounds.js",
            subtitle: "Set Round for " + req.params.tournament
            });
        })
    .post(authUser, function(req, res){
        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament,
            data: {rounds: req.body.rounds || ""}
            });
        });
router.route("/tournament/:tournament/rounds/content")
    .get(authUser, function(req, res) {
        var url = "/tournament/" + req.params.tournament;

        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: url,
            onSuccess: function(responseBody) {
                var responseDict = JSON.parse(responseBody);
                responseDict.tournament = req.params.tournament,

                res.status(200).json(responseDict);
                },
            });
    });

router.route("/tournament/:tournament/round/:round/draw")
    .get(function(req, res) {
       res.render("basic", {
            src_loc: "/tournamentDraw.js",
            subtitle: "Draw for Round " + req.params.round + ", "
                      + req.params.tournament
        });
    });
router.route("/tournament/:tournament/round/:round/draw/content")
    .get(function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/rounds/"
                + req.params.round;

        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: url,
            onSuccess: function(responseBody) {
                var responseDict = JSON.parse(responseBody);
                responseDict.tournament = req.params.tournament,
                responseDict.round = req.params.round;

                res.status(200).json(responseDict);
                },
            });
    });

router.route("/tournament/:tournament/categories")
    .get(authUser, function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentCategories.js",
            subtitle: "Set Categories for " + req.params.tournament
            });
        })
    .post(authUser, function(req, res){
        try {
            var cleanCats = Category.cleanCategories(req.body.categories);
            DAOAmbassador.request({
                method: "POST",
                request: req,
                response: res,
                URL: "/tournament/" + req.params.tournament,
                data: {score_categories: cleanCats}
                });
        }
        catch (err) {
            res.status(400).json({error: err});
            return;
        }
        });
router.route("/tournament/:tournament/categories/content")
    .get(authUser, function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/score_categories";

        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: url,
            onSuccess: function(responseBody) {
                var responseDict = {
                        instructions: "Set the score categories for " +
                            req.params.tournament +
                            " here. For example, \"Battle\", \"Sports\", etc.",
                        tournament: req.params.tournament
                    },
                    categories = JSON.parse(responseBody) || [],
                    numLines = 5,
                    paddedCats = [];

                // We want a minimum of 5 categories to be displayed
                for (var i = 0; i < numLines; i++) {
                    paddedCats.push(Category.emptyScoreCategory());
                }
                categories.forEach(function(cat, idx) {
                    paddedCats[idx] = cat;
                });
                responseDict.categories = paddedCats.sort(function(a, b){
                    var nameA = a.name.toUpperCase(),
                        nameB = b.name.toUpperCase();

                    if (nameA < nameB || nameB === "") {
                      return -1;
                    }
                    else if (nameA > nameB || nameA === "") {
                      return 1;
                    }
                    else {
                        return 0;
                    }

                    });

                res.status(200).json(responseDict);
                }
            });
    });

router.route("/tournament/:tournament/missions")
    .get(authUser, function(req, res) {
        res.render("basic", {
            src_loc: "/tournamentMissions.js",
            subtitle: "Set Missions for " + req.params.tournament
            });
        })
    .post(authUser, function(req, res){

        DAOAmbassador.request({
            method: "POST",
            request: req,
            response: res,
            URL: "/tournament/" + req.params.tournament,
            data: req.body,
            });
        });
router.route("/tournament/:tournament/missions/content")
    .get(authUser, function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/missions";

        DAOAmbassador.request({
            method: "GET",
            request: req,
            response: res,
            URL: url,
            onSuccess: function(responseBody) {
                var responseDict = {
                    missions: JSON.parse(responseBody),
                    tournament: req.params.tournament,
                    message: "Set the missions for " + req.params.tournament
                                + " here:"
                };
                res.status(200).json(responseDict);
                }
            });
    });

module.exports = router;
