// Tournament information
var DAOAmbassador = require("./dao-ambassador"),
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
            DAOAmbassador.postToDAORequest(
                req,
                res,
                "/tournament",
                {
                    inputTournamentName: req.body.name,
                    inputTournamentDate: req.body.date
                },
                undefined,
                function(responseBody) {
                    res.status(400).json({error: responseBody});
                });
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
                "/tournament/" + req.params.tournament + "/register",
                {inputUserName: req.user.username});
        });
router.route("/tournament/:tournament/content")
    .get(function(req, res) {
        DAOAmbassador.getFromDAORequest(
            req,
            res,
            "/tournament/" + req.params.tournament,
            function(result) {
                res.status(200).json(result);
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
                "/tournament/" + req.params.tournament + "/rounds",
                {numRounds: req.body.rounds});
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


module.exports = router;
