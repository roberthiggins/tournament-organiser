/* Ambassador-like module for interacting with the DAO */
const winston = require("winston"),
      querystring = require("querystring");
/*
 * Gets a ClientRequest to the DAO.
 * Caller is responsible for attaching success and fail handlers
 */
exports.postToDAORequest = function(path, JSONData, onSuccess, onFail) {

    var http            = require("http"),
        querystring     = require("querystring"),
        daoName         = process.env.DAO_CONTAINER,
        daoIP           = process.env[daoName + "_PORT_5000_TCP_ADDR"],
        daoPort         = process.env[daoName + "_PORT_5000_TCP_PORT"],
        postData        = querystring.stringify(JSONData),
        postOptions     = {
            host: daoIP,
            port: daoPort,
            path: path,
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": Buffer.byteLength(postData)
            }
        };

    var req = http.request(postOptions, function(res) {
        var body = '';
        res.setEncoding("utf8");
        res.on('data', function(chunk) {
            body += chunk;
        });

        res.on("end", function() {
            if (typeof onSuccess === "function" && res.statusCode === 200) {
                winston.log("info", "Request to DAO succeeded", path);
                onSuccess(body);
            } else if (typeof onFail === "function") {
                winston.log("info", "Request to DAO failed.", path);
                onFail(body);
            }
        })
    });

    req.on("error", function(err) {
        winston.log("error", "Problem with request to DAO", err.message);
    });

    req.write(postData);
    req.end();
};
