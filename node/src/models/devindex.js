exports.enterT = {
    title: "Enter a Tournament",
    actions: [
        {text: "See a list of tournaments", href: "/tournaments"},
        {text: "Register To Play In register_test_1",
         href: "/tournament/register_test_1"},
        {text: "Update my player details"},
        {text: "Update application"},
        {text: "See application status"},
        {text: "See upcoming tournaments for user user_1",
         href: "user/user_1/tournaments"},
    ]
};
exports.orgT = {
    title: "Organise a Tournament",
    actions: [
        {href: "/tournament/create", text: "Create a Tournament"},
        {href: "/tournament/ranking_test/rounds",
         text: "Set num rounds for ranking_test"},
        {href: "/tournament/mission_test/categories",
         text: "Set scoring categories for mission_test"},
        {href: "/tournament/mission_test/missions",
         text: "Set missions for mission_test"},
        {href: "/tournament/northcon_2095/missions",
         text: "Setup Northcon_2095"}
    ]
};
exports.playT = {
    title: "Play in a Tournament",
    actions: [
        {text: "Get a game for ranking_test",
         href: "/tournament/ranking_test/round/1/draw"},
        {text: "Get next game for ranking_test_player_1",
         href: "/tournament/ranking_test/entry/ranking_test_player_1/nextgame"},
        {text: "Get the table layout"},
        {text: "Get a mission for ranking_test round 1",
         href: "/tournament/ranking_test/round/1/draw"},
        {text: "Get an opponent army list"},
        {text: "Get their army list (may be different between games)"},
        {text: "Get the time remaining in the round"},
        {text: "Submit a score for ranking_test entry ranking_test_player_1",
         href: "/tournament/ranking_test/entry/ranking_test_player_1/enterscore"},
        {text: "See total scores for ranking_test",
         href: "/tournament/ranking_test/rankings"},
        {text: "Review previous games"}
    ]
};
exports.viewT = {
    title: "Information",
    actions: [
            {text: "See the current placings for ranking_test",
             href: "/tournament/ranking_test/rankings"},
            {text: "See Northcon 2095",
             href: "/tournament/northcon_2095"},
            {text: "See the 1st Round draw for ranking_test",
             href: "/draw/ranking_test/1"},
            {text: "See entries for ranking_test",
             href: "/tournament/ranking_test/entries"},
            {text: "Search for tournaments - by player, army, club, etc."},
            {text: "View results of tournies they've played in."}
    ]
};
exports.feedback = {
    title: "Feedback",
    actions: [
        {text: "Place Feedback", href: "/feedback"},
        {text: "about players"},
        {text: "about to"},
        {text: "about tournie"}
    ]
};
