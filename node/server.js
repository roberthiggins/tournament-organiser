var bodyParser = require("body-parser"),
    express = require("express"),
    expressSession = require("express-session"),
    passport = require("passport");
const app = express();

app.listen(process.env.PORT || 8000);

// Additional middleware which will set headers that we need on each request.
app.use(function(req, res, next) {
    // Set permissive CORS header - this allows this server to be used only as
    // an API server in conjunction with something like webpack-dev-server.
    res.setHeader("Access-Control-Allow-Origin", "*");

    // Disable caching so we"ll always get the latest comments.
    res.setHeader("Cache-Control", "no-cache");
    next();
});

app.set("views", "./src/views/jade");
app.set("view engine", "jade");
app.use("/", express.static("public"));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

// Express sessions for session management
app.use(expressSession({
    secret: "mySecretKeyTODO", // TODO get something from env vars
    maxAge: 15 * 60 * 1000,
    resave: false,
    saveUninitialized: false
// TODO MemoryStore is the default but isn't prod ready
}));

// Routing
app.use("/", require('./src/public-routes'));
app.use("/", require('./src/member-only-routes'));

// Passport user auth
app.use(passport.initialize());
app.use(passport.session());
