var DAOAmbassador = require("../lib/dao-ambassador"),
    express       = require("express"),
    Menu          = require("../models/menu"),
    router        = express.Router(),
    users         = require("../lib/users");

router.route("/content")
    .get(users.injectUserIntoRequest, function(req, res) {

        if (req.user) {

            DAOAmbassador.request({
                method: "GET",
                request: req,
                response: res,
                URL: "/user/" + req.user.username + "/actions",
                onSuccess: function(body) {
                        res.status(200).json(Menu.transform(JSON.parse(body)));
                    }
                });
        }
        else {
            res.status(200).json(Menu.defaultMenu());
        }
    });


module.exports = router;
