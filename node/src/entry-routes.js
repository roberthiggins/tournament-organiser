// Tournament information
var DAOAmbassador = require("./dao-ambassador"),
    express       = require('express'),
    router        = express.Router();


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

module.exports = router;
