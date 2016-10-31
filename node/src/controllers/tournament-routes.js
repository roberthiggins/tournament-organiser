// Tournament information
var Category      = require("../models/score-categories"),
    DAOAmbassador = require("../lib/dao-ambassador"),
    express       = require('express'),
    router        = express.Router(),
    users         = require("./users");


router.route("/tournaments")
    .get(function(req, res) {
        res.render("basic", {src_loc: "/tournamentList.js"});
    });
router.route("/tournaments/content")
    .get(function(req, res) {
        DAOAmbassador.getFromDAORequest(req, res, "/tournament/",
            function(result) {
                res.status(200).json(result);
            });
    });

router.route("/tournament/create")
    .get(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res) {
            res.render("basic", {
                src_loc: "/tournamentCreate.js",
                subtitle: "Add a Tournament"
            });
        })
    .post(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res){

            try {
                var cleanCats = Category.cleanCategories(req.body.categories);
                DAOAmbassador.postToDAORequest(
                    req,
                    res,
                    "/tournament",
                    {
                        inputTournamentName: req.body.name,
                        inputTournamentDate: req.body.date,
                        rounds: req.body.rounds || 0,
                        score_categories: cleanCats
                    },
                    function success(result) {
                        res.status(200).json(JSON.parse(result));
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
    .post(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res){
            DAOAmbassador.postToDAORequest(
                req,
                res,
                "/tournament/" + req.params.tournament + "/register/" +
                req.user.username,
                {});
        });
router.route("/tournament/:tournament/content")
    .get(function(req, res) {
        DAOAmbassador.getFromDAORequest(
            req,
            res,
            "/tournament/" + req.params.tournament,
            function(result) {
                res.status(200).json(JSON.parse(result));
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
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

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                var responseDict = {entries: JSON.parse(responseBody)};
                responseDict.tournament = req.params.tournament,

                res.status(200).json(responseDict);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
            });
    });

router.route("/tournament/:tournament/rounds")
    .get(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res) {
            res.render("basic", {
                src_loc: "/tournamentRounds.js",
                subtitle: "Set Round for " + req.params.tournament
            });
        })
    .post(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res){
            DAOAmbassador.postToDAORequest(
                req,
                res,
                "/tournament/" + req.params.tournament,
                {rounds: req.body.rounds});
        });
router.route("/tournament/:tournament/rounds/content")
    .get(function(req, res) {
        var url = "/tournament/" + req.params.tournament;

        DAOAmbassador.getFromDAORequest(req, res, url,
            function(responseBody) {
                var responseDict = JSON.parse(responseBody);
                responseDict.tournament = req.params.tournament,

                res.status(200).json(responseDict);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
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

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(responseBody) {
                var responseDict = JSON.parse(responseBody);
                responseDict.tournament = req.params.tournament,
                responseDict.round = req.params.round;

                res.status(200).json(responseDict);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
            });
    });

router.route("/tournament/:tournament/categories")
    .get(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res) {
            res.render("basic", {
                src_loc: "/tournamentCategories.js",
                subtitle: "Set Categories for " + req.params.tournament
            });
        })
    .post(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res){

            try {
                var cleanCats = Category.cleanCategories(req.body.categories);
                DAOAmbassador.postToDAORequest(
                    req,
                    res,
                    "/tournament/" + req.params.tournament,
                    {score_categories: cleanCats});
            }
            catch (err) {
                res.status(400).json({error: err});
                return;
            }
        });
router.route("/tournament/:tournament/categories/content")
    .get(function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/score_categories";

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(responseBody) {
                var responseDict = {
                        instructions: "Set the score categories for "
                            + req.params.tournament
                            + " here. For example, \"Battle\", \"Sports\", etc.",
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
            });
    });

router.route("/tournament/:tournament/missions")
    .get(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res) {
            res.render("basic", {
                src_loc: "/tournamentMissions.js",
                subtitle: "Set Missions for " + req.params.tournament
            });
        })
    .post(
        users.injectUserIntoRequest,
        users.ensureAuthenticated,
        function(req, res){

            var url = "/tournament/" + req.params.tournament,
                missionList = function(postData) {

                    var idx = 0,
                        missions = [],
                        missionsInPost = true;

                    while (missionsInPost) {
                        var mission = postData["missions_" + idx];
                        if (typeof mission !== "undefined") {
                            missions.push(mission);
                            idx = idx +1;
                        }
                        else {
                            missionsInPost = false;
                        }
                    }

                    return missions;
                },
                postData = {missions: missionList(req.body)};

            DAOAmbassador.postToDAORequest(req, res, url, postData);
        });
router.route("/tournament/:tournament/missions/content")
    .get(function(req, res) {
        var url = "/tournament/" + req.params.tournament + "/missions";

        DAOAmbassador.getFromDAORequest(
            req,
            res,
            url,
            function(responseBody) {
                var responseDict = {
                    missions: JSON.parse(responseBody),
                    tournament: req.params.tournament,
                    message: "Set the missions for " + req.params.tournament
                                + " here:"
                };
                res.status(200).json(responseDict);
            },
            function(responseBody) {
                res.status(200).json({error: responseBody});
            });
    });

module.exports = router;
