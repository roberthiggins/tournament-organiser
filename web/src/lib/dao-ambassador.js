/* Ambassador-like module for interacting with the DAO */
var logger = require("./logger");

// Make a request to the DAO server
var DAORequestConfig = function(req, res, path, method, headers, onSuccess,
                                onFail) {

    var http    = require("http"),
        daoIP   = process.env["DAOSERVER_PORT_5000_TCP_ADDR"],
        daoPort = process.env["DAOSERVER_PORT_5000_TCP_PORT"],
        opts    = {
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
            res.status(400).json({error: responseBody});
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
            var meth = (method + "    ").substring(0, 4);
            if (typeof onSuccess === "function" && DAOres.statusCode === 200) {
                logger.info(" " + meth + " Request to DAO succeeded", path);
                onSuccess(body);
            } else if (typeof onFail === "function") {
                logger.error(meth + " Request to DAO failed.", path, body);
                onFail(body);
            }
        })
    });

    DAOreq.on("error", function(err) {
        logger.error("Problem with request to DAO", err.message);
    });

    return DAOreq;
};

var makeAuth = function (req) {
    var user = req && req.session && req.session.user ? req.session.user : null,
        auth = user ? "Basic " + new Buffer(user.username + ":" +
                user.password).toString("base64") : null;

    return auth;
};

/*
 * GET request to the DAO server.
 * Caller is responsible for attaching success and fail handlers
 */
exports.getFromDAORequest = function(req, res, path, onSuccess, onFail) {

    var headers = {
            "Content-Type": "application/json",
            "Authorization": makeAuth(req)
        },
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

    var postData = JSON.stringify(JSONData),
        headers  = {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(postData),
            "Authorization": makeAuth(req)
        },
        DAOreq   = DAORequestConfig(req, res, path, "POST", headers, onSuccess,
            onFail);

    DAOreq.write(postData);
    DAOreq.end();
};
