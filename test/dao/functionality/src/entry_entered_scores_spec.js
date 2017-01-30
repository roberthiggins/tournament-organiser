var injector = require("./data_injector"),
    tourn = "existing_score_test",
    p1 = tourn + "_player_1",
    p2 = tourn + "_player_2",
    get = injector.enteredScores.bind(this, tourn, p1),
    expected = {
        per_tournament: {},
        per_game: [
            { Battle: 20, game_id: Number, 'Fair Play': 5 },
            { Battle: 15, game_id: Number, 'Fair Play': 5 }],
    };

describe("Auth problems", function () {
    "use strict";

    get(null, "No auth tries to see scores", 401,
        "Could not verify your access level");
    get(p2, "another", 403, "Permission denied");
    get(p1, "The player", 200, expected);
    get("superuser", "Superuser", 200, expected);
    get(tourn + "_to", "TO", 200, expected);
});

describe("See per_game scores", function () {
    "use strict";

    get(p1, "The player", 200, expected);

    var p_4 = tourn + "_player_4",
    p_4Expected = {
        per_tournament: {},
        per_game: [
            { Battle: 20, game_id: Number, 'Fair Play': 5 },
            { Battle: 5, game_id: Number, 'Fair Play': null }],
            // They haven't entered sports for p_5
    };
    injector.enteredScores(tourn, p_4, p_4, p_4 + " scores", 200, p_4Expected);

    var p_5 = tourn + "_player_5",
    p_5Expected = {
        per_tournament: {},
        per_game: [
            { Battle: 0, game_id: Number, 'Fair Play': 1 },
            { Battle: 15, game_id: Number, 'Fair Play': 5 }],
    };
    injector.enteredScores(tourn, p_5, p_5, p_5 + " scores", 200, p_5Expected);

});
