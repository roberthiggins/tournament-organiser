/* Functions for assisting with user login and auth. */

exports.placeFeedback = function(req, res) {

    var DAOAmbassador = require("./dao-ambassador");

    DAOAmbassador.postToDAORequest(
        req,
        res,
        "/feedback",
        {inputFeedback: req.body.feedback},
        undefined,
        function(responseBody) {
            return res.status(400).json({message: responseBody});
        });
};
