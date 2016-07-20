var express = require("express");
const app = express();

app.listen(process.env.PORT || 3000);

// Additional middleware which will set headers that we need on each request.
app.use(function(req, res, next) {
    // Set permissive CORS header - this allows this server to be used only as
    // an API server in conjunction with something like webpack-dev-server.
    res.setHeader("Access-Control-Allow-Origin", "*");

    // Disable caching so we"ll always get the latest comments.
    res.setHeader("Cache-Control", "no-cache");
    next();
});

app.set('views', './views');
app.set('view engine', 'jade');
app.use("/", express.static("public"));

app.get("/indexcontent", function(req, res) {
    var content = require("./src/models/devindex.js");
    res.send([
        content.enterT,
        content.orgT,
        content.playT,
        content.viewT,
        content.feedback
    ]);
});
app.route("/").get(function(req, res) {
    res.render("devindex");
});
app.route("/devindex").get(function(req, res) {
    res.render("devindex");
});
app.route("/login")
    .get(function(req, res) {
        res.render("login");
    });
