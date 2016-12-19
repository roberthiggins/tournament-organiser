var injector = require("./data_injector");

var setup = function setup(tourn, players) {
    var categories = [
        [tourn + "_per_tourn_1", 1, true, 4, 15],
        [tourn + "_per_tourn_2", 1, true, 4, 15],
        [tourn + "_per_tourn_su", 1, true, 1, 5],
        [tourn + "_per_tourn_to", 1, true, 1, 5],
        [tourn + "_per_game_1", 1, false, 4, 15, true],
    ];
    injector.createTournament(tourn, "2095-10-10", 1, null, categories, players);
};

describe("Enter a tournament score for an entry", function () {
    "use strict";

    var tourn = "enter_score_test_4",
        p1 = tourn + "_p_1",
        post = injector.enterScore.bind(this, true, tourn, p1);

    setup(tourn, [p1, tourn + "_p_2"]);

    post("superuser", "Superuser", [[tourn + "_per_tourn_su", 5]], 200,
        "Score entered for " + p1 + ": 5");
    post(tourn + "_to", "TO", [[tourn + "_per_tourn_to", 5]], 200,
        "Score entered for " + p1 + ": 5");
});

describe("Auth Problems", function () {
    "use strict";

    var tourn = "enter_score_test_5",
        p1 = tourn + "_p_1",
        p2 = tourn + "_p_2",
        post = injector.enterScore.bind(this, true, tourn, p1);

    setup(tourn, [p1, p2]);
    injector.createUser("enter_score_random");

    post(null, "No auth enters a score", [[null, 5]], 401,
        "Could not verify your access level");
    post("enter_score_random", "Rand user", [[null, 5]], 403, "Permission denied");
    post(p2, "Different entry", [[null, 5]], 403, "Permission denied");
});

describe("Enter a tournament score for an entry", function () {
    "use strict";

    var tourn = "enter_score_test_6",
        p1 = tourn + "_p_1",
        post = injector.enterScore.bind(this, true, tourn, p1, p1);

    setup(tourn, [p1, tourn + "_p_2"]);

    post("Score too low", [[null, 0]], 400, "Invalid score: 0");
    post("Score too high", [[null, 16]], 400, "Invalid score: 16");
    post("Player", [[null, 5]], 200, "Score entered for " + p1 + ": 5");

    post("Player enters a score twice", [[null, 4]], 400,
        "4 not entered. Score is already set");
    post("Fake category", [["non_ex", 5]], 400, "Unknown category: non_ex");
    post("Per game category", [[tourn + "_per_game_1", 5]], 400,
        tourn + "_per_game_1 should be entered per-tournament");
});

describe("Enter multiple scores", function () {
    "use strict";

    var tourn = "enter_score_test_7",
        p1 = tourn + "_p_1",
        cat1 = tourn + "_per_tourn_1",
        cat2 = tourn + "_per_tourn_2",
        post = injector.enterScore.bind(this, true, tourn, p1, p1);

    setup(tourn, [p1, tourn + "_p_2"]);

    post("Missing score", [[cat1, 5], [cat2, null]], 400,
        "Score not entered: None");
    post("Illegal score", [[cat1, 0], [cat2, 5]], 400, "Invalid score: 0");
    post("Multi Scores", [[cat1, 5], [cat2, 5]], 200, "Score entered for " + p1);
    post("Enter twice", [[cat1, 4]], 400, "4 not entered. Score is already set");
    post("Enter twice", [[cat2, 4]], 400, "4 not entered. Score is already set");
    post("Illegal score", [[cat2, 0], [cat2, 5]], 400, "Invalid score: 0");
});
