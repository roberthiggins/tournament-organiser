var djangoURL = "http://" + process.env.DJANGO_WEBSERVER + ":"
    + process.env.DJANGO_WEBSERVER_PORT;

exports.enterT = {
    djangoURL: djangoURL,
    title: "Enter a Tournament",
    actions: [
        {text: "See a list of tournaments", href: "tournaments"},
        {text: "Register for a Tournament", href: "registerforatournament"},
        {text: "Update my player details"},
        {text: "Update application"},
        {text: "See application status"},
    ]
};
exports.orgT = {
    djangoURL: djangoURL,
    title: "Organise a Tournament",
    actions: [
        {href: "createtournament", text: "Create a Tournament"},
        {href: "setrounds/mission_test",
         text: "Set num rounds for mission_test"},
        {href: "setcategories/mission_test",
         text: "Set scoring categories for mission_test"},
        {href: "setmissions/mission_test",
         text: "Set missions for mission_test"},
        {href: "tournamentsetup/northcon_2095",
         text: "Setup Northcon_2095"}
    ]
};
exports.playT = {
    djangoURL: djangoURL,
    title: "Play in a Tournament",
    actions: [
        {text: "Get a game"},
        {text: "Get a table"},
        {text: "Get an opponent"},
        {text: "Get the table layout"},
        {text: "Get a mission"},
        {text: "Get an opponent army list"},
        {text: "Get their army list (may be different between games)"},
        {text: "Get the time remaining in the round"},
        {text: "Submit a score"},
        {text: "Submit a soft score"},
        {text: "Submit a once off score for ranking_test entry homer",
         href: "enterscore/ranking_test/homer"},
        {text: "See their total score"},
        {text: "Review previous games"}
    ]
};
exports.viewT = {
    djangoURL: djangoURL,
    title: "Feedback",
    actions: [
            {text: "See the current placings for ranking_test",
             href: "rankings/ranking_test"},
            {text: "See Northcon 2095", href: "tournament/northcon_2095"},
            {text: "See the 1st Round draw for ranking_test",
             href: "draw/ranking_test/1"},
            {text: "See entries for ranking_test",
             href: "ranking_test/entries"},
            {text: "Search for tournaments - by player, army, club, etc."},
            {text: "View results of tournies they've played in."}
    ]
};
exports.feedback = {
    djangoURL: djangoURL,
    title: "Feedback",
    actions: [
        {text: "Place Feedback", href: "feedback"},
        {text: "Suggest Improvement", href: "suggestimprovement"},
        {text: "about players"},
        {text: "about to"},
        {text: "about tournie"}
    ]
};
