Feature: Enter the score for a game
    I want to enter the scores for an individual game
    As a player or TO
    So I can get scores

    Scenario Outline: The TO enters scores for the game
        When I POST "<value>" to "/entergamescore" from the API
        Then the API response should contain "<response_text>"
        Then the API response status code should be <code>
        Examples:
            |code |response_text               |value          |
            |400  | Enter the required fields  |foo            |
            |400  | Enter the required fields  |               |
            |400  | Enter the required fields  | gamescore={%22round%22: %221%22, %22scores%22: {%22stevemcqueen%22: %2220%22}}              |
            |400  | Enter the required fields  | gamescore={%22tournament_name%22: %22foo%22, %22scores%22: {%22stevemcqueen%22: %2220%22, %22jerry%22: %2220%22}}              |
            |400  | Enter the required fields  | gamescore={%22tournament_name%22: %22foo%22, %22round%22: %221%22}|
            |400  | Enter the required fields  | gamescore={%22tournament_name%22: %22foo%22, %22round%22: %221%22, %22scores%22: {}}|
            |400  | Enter the required fields  | gamescore={%22tournament_name%22: %22foo%22, %22round%22: %221%22, %22scores%22: {%22stevemcqueen%22: %2220%22}}|
            |400  | Unknown tournament: foo    | gamescore={%22tournament_name%22: %22foo%22, %22round%22: %221%22, %22scores%22: {%22stevemcqueen%22: %2220%22, %22rick_james%22: %2220%22}}|
            |400  | Unknown player: bobnoname  | gamescore={%22tournament_name%22: %22painting_test%22, %22round%22: %221%22, %22scores%22: {%22bobnoname%22: %2220%22, %22stevemcqueen%22: %2220%22}}|
            |400  | Enter the required fields  | gamescore={%22tournament_name%22: %22painting_test%22, %22round%22: %221%22, %22scores%22: {%22stevemcqueen%22: %2220%22, %22stevemcqueen%22: %2220%22}}|


# Awaiting user controls
#    Scenario: One of the players enters scores for the game
#    Scenario: An unrelated person enters scores for a game
