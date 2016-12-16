/* Functions for assisting with user login and auth. */

var DAOAmbassador = require("./dao-ambassador"),
    passport      = require("passport"),
    LocalStrategy = require("passport-local").Strategy,
    winston       = require("winston");

// Middleware to inject the user into the request
exports.injectUserIntoRequest = function(req, res, next) {
    if (req.session && req.session.user) {
        req.user = JSON.parse(JSON.stringify(req.session.user));
        delete req.user.password;
        res.locals.user = req.user;
    }
    next();
};

// Middleware to ensure user is authenticated.
exports.ensureAuthenticated = function(req, res, next) {
    if (!req.isAuthenticated()) {
        res.redirect("/login?next=" + req.url);
    } else {
        next();
    }
}

exports.logout = function(req, res) {
    req.logOut(); // Why you no work?
    delete req.user;
    delete res.locals.user;
    req.session.destroy(function () {
        res.redirect('/');
    });
}

passport.serializeUser(function(user, done) {
    winston.log("info", "serializing ", user.username);
    done(null, user.username);
});

passport.deserializeUser(function(obj, done) {
    winston.log("info", "deserializing ", obj);
    done(null, obj);
});

passport.use('local-signin', new LocalStrategy(
    {passReqToCallback : true}, //allows us to pass back the request to the cb
    function(req, username, password, done) {
        // Checks for empty fields are handled by Passport before this.

        var userDetails = {
                inputUsername: username,
                inputPassword: password
            };
        DAOAmbassador.request({
            method: "POST",
            URL: "/user/" + req.body.username + "/login",
            data: userDetails,
            onSuccess: function success() {
                return done(null, {username: username, password: password});
                },
            onFail: function failure(responseBody) {
                return done(null, false, {message: responseBody});
                }
            });
    }
));


exports.login = function(req, res, next) {
    passport.authenticate("local-signin", function(err, user, info) {

        if (err) { return next(err); }

        if (!user) { return res.status(400).json(info); }

        req.session.user = user;
        return res.status(200).send("Login Successful");
    })(req, res, next);
};


exports.signup = function(req, res) {

    if (!req.body.username) {
        res.status(400).json({error: "Please enter a username"});
        return false;
    }

    DAOAmbassador.request({
        method: "POST",
        request: req,
        response: res,
        URL: "/user/" + req.body.username,
        data: req.body,
        onFail: function failure(responseBody) {
            res.status(400).json({error: responseBody});
            }
        });
};
