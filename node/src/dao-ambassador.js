/* Ambassador-like module for interacting with the DAO */
const winston = require("winston"),
      querystring = require("querystring");

// Make a request to the DAO server
var DAORequestConfig = function(req, res, path, method, headers, onSuccess,
                                onFail) {

    var http            = require("http"),
        daoIP           = process.env["DAOSERVER_PORT_5000_TCP_ADDR"],
        daoPort         = process.env["DAOSERVER_PORT_5000_TCP_PORT"],
        opts            = {
            host: daoIP,
            port: daoPort,
            path: path,
            method: method,
            headers: headers
        },
        defaultOnSuccess = function(responseBody) {
            res.status(200).json({message: responseBody});
        },
        defaultOnFail = function(responseBody) {
            res.status(200).json({message: responseBody});
        };
    onSuccess = typeof onSuccess === "function" ? onSuccess : defaultOnSuccess;
    onFail = typeof onFail === "function" ? onFail : defaultOnFail;

    var DAOreq = http.request(opts, function(DAOres) {
        var body = "";
        DAOres.setEncoding("utf8");
        DAOres.on("data", function(chunk) {
            body += chunk;
        });

        DAOres.on("end", function() {
            if (typeof onSuccess === "function" && DAOres.statusCode === 200) {
                winston.log("info", "Request to DAO succeeded", path);
                onSuccess(body);
            } else if (typeof onFail === "function") {
                winston.log("info", "Request to DAO failed.", path);
                onFail(body);
            }
        })
    });

    DAOreq.on("error", function(err) {
        winston.log("error", "Problem with request to DAO", err.message);
    });

    return DAOreq;
};

/*
 * GET request to the DAO server.
 * Caller is responsible for attaching success and fail handlers
 */
exports.getFromDAORequest = function(req, res, path, onSuccess, onFail) {

    var headers = {"Content-Type": "application/json"},
        DAOreq = DAORequestConfig(req, res, path, "GET", headers, onSuccess,
            onFail);

    DAOreq.end();
};

/*
 * POST request to the DAO server.
 * Caller is responsible for attaching success and fail handlers
 */
exports.postToDAORequest = function(req, res, path, JSONData, onSuccess,
                                    onFail) {

    var user     = req && req.user ? req.user : null,
        postData = querystring.stringify(JSONData),
        auth     = user ? "Basic " + new Buffer(user.username + ":" +
                    user.password).toString("base64") : null,
        headers  = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": Buffer.byteLength(postData),
            "Authorization": auth
        },
        DAOreq = DAORequestConfig(req, res, path, "POST", headers, onSuccess,
            onFail);

    DAOreq.write(postData);
    DAOreq.end();
};
