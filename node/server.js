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
// TODO MemoryStore is the default but is not prod ready
}));

// Routing
app.use("/", require("./src/controllers/entry-routes"));
app.use("/", require("./src/controllers/member-only-routes"));
app.use("/", require("./src/controllers/public-routes"));
app.use("/", require("./src/controllers/tournament-routes"));
app.use("/menu", require("./src/controllers/menu"));

// Passport user auth
app.use(passport.initialize());
app.use(passport.session());

// 404 handling
app.use(function(req, res){
    res.status(404);

    res.format({
        "text/html": function(){
            res.render("404", { url: req.url });
        },
        "application/json": function(){
            res.send({ error: "Not found" });
        },
        "default": function() {
            // log the request and respond with 406
            res.status(406).send("Not Acceptable");
        }
    });
});
