/* Functions for assisting with user login and auth. */

var DAOAmbassador = require("./dao-ambassador"),
    passport      = require("passport"),
    LocalStrategy = require("passport-local").Strategy,
    winston       = require("winston");

// Middleware to inject the user into the request
exports.injectUserIntoRequest = function(req, res, next) {
    if (req.session && req.session.user) {
        var user = req.session.user; // TODO actually verify the user exists
        req.user = user;
        delete req.user.password;
        req.session.user = user;  //refresh the session value
        res.locals.user = user;
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
        res.redirect('/devindex');
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
        DAOAmbassador.postToDAORequest(
            null,
            null,
            "/user/" + req.body.username + "/login",
            userDetails,
            function success() {
                return done(null, {username: username, password: password});
            },
            function failure(responseBody) {
                return done(null, false, {message: responseBody});
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
    var userDetails = {
            email: req.body.email,
            password1: req.body.password1,
            password2: req.body.password2
        };
    DAOAmbassador.postToDAORequest(
        req,
        res,
        "/user/" + req.body.username,
        userDetails);
};
