var bodyParser = require("body-parser"),
    express = require("express"),
    expressSession = require("express-session"),
    users = require("./src/users.js"),
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

app.set("views", "./views");
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

// Passport user auth
app.use(passport.initialize());
app.use(passport.session());
app.use(users.injectUserIntoRequest)

app.route("/")
    .get(function(req, res) { res.render("devindex"); });
app.route("/devindex")
    .get(function(req, res) { res.render("devindex"); });
app.route("/devindex/content")
    .get(function(req, res) {
        var content = require("./src/models/devindex.js");
        res.send([
            content.enterT,
            content.orgT,
            content.playT,
            content.viewT,
            content.feedback
        ]);
    });
app.route("/login")
    .get(function(req, res) { res.render("login"); })
    .post(users.login);
