/* Functions for assisting with user login and auth. */

exports.login = function (req, res) {

    req.assert("username", "This field is required").notEmpty();
    req.assert("password", "This field is required").notEmpty();

    var errors = req.validationErrors();
    if(errors){
        res.status(400).json(errors);
        return;
    }

    var DAOAmbassador = require("./src/dao-ambassador"),
        userDetails = {
            inputUsername: req.body.username,
            inputPassword: req.body.password
        };
    DAOAmbassador.postToDAORequest(
        "/user/" + req.body.username + "/login",
        userDetails,
        function success() {
            res.status(200).send("/devindex");
        },
        function failure(responseBody) {
            res.status(400).json([{param: "general", msg: responseBody}]);
        });
};
