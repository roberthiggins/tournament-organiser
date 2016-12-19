var injector = require("./data_injector"),
    tourn = "enter_score_test_1",
    p1 = tourn + "_p_1",
    p2 = tourn + "_p_2";

describe("Enter a tournament score for an entry", function () {
    "use strict";

    var post = injector.enterScore.bind(this, true, tourn, p1);
    post("superuser", "Superuser", [[tourn + "_per_tourn_su", 5]], 200,
        "Score entered for " + p1 + ": 5");
    post(tourn + "_to", "TO", [[tourn + "_per_tourn_to", 5]], 200,
        "Score entered for " + p1 + ": 5");
});

describe("Auth Problems", function () {
    "use strict";

    var post = injector.enterScore.bind(this, true, tourn, p1);
    post(null, "No auth enters a score", [[null, 5]], 401,
        "Could not verify your access level");
    post("charlie_murphy", "Rand user", [[null, 5]], 403, "Permission denied");
    post(p2, "Different entry", [[null, 5]], 403, "Permission denied");
});

describe("Enter a tournament score for an entry", function () {
    "use strict";

    var post = injector.enterScore.bind(this, true, tourn, p1, p1);
    post("Score too low", [[null, 0]], 400, "Invalid score: 0");
    post("Score too high", [[null, 16]], 400, "Invalid score: 16");
    post("Player", [[null, 5]], 200, "Score entered for " + p1 + ": 5");

    post("Player enters a score twice", [[null, 4]], 400,
        "4 not entered. Score is already set");
    post("Fake category", [["non_ex", 5]], 400, "Unknown category: non_ex");
    post("Per game category", [[tourn + "_per_game_1", 5]], 400,
        tourn + "_per_game_1 should be entered per-tournament");
});
