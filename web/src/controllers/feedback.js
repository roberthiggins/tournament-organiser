/* Functions for assisting with user login and auth. */

exports.placeFeedback = function(req, res) {

    require("../lib/dao-ambassador").request({
        method: "POST",
        request: req,
        response: res,
        URL: "/feedback",
        data: {inputFeedback: req.body.feedback},
        onFail: function(responseBody) {
            return res.status(400).json({message: responseBody});
            }
        });
};
