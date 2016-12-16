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

/*
 * Add auth string to request
 */
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
var getFromDAORequest = function(req, res, path, onSuccess, onFail) {

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
var postToDAORequest = function(req, res, path, method, JSONData, onSuccess,
                                onFail) {

    var postData = JSON.stringify(JSONData),
        headers  = {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(postData),
            "Authorization": makeAuth(req)
        },
        DAOreq   = DAORequestConfig(req, res, path, method, headers, onSuccess,
            onFail);

    DAOreq.write(postData);
    DAOreq.end();
};

/*
 * Make a request to the Daoserver. Takes arguments in an object
 * {
 *      method    - string   - "GET", "POST", etc.
 *      URL       - string   - target (REQUIRED),
 *      request   - object   - request object,
 *      response  - object   - response object,
 *      data      - object   - data to post
 *      onSuccess - function - to run after 200,
 *      onFail    - function - to run after failure code
 * }
 */
exports.request = function(o) {
    if (o.method === "GET") {
        getFromDAORequest(o.request, o.response, o.URL, o.onSuccess, o.onFail);
    } else if (o.method === "POST" || o.method === "PUT") {
        postToDAORequest(o.request, o.response, o.URL, o.method, o.data || {},
            o.onSuccess || undefined, o.onFail || undefined);
    } else {
        throw "Request method required: GET, POST, PUT, etc.";
    }
};
