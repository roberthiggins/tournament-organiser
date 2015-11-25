Feature: Setup the scores a player can get in a tournament
    In order to let players get scores
    As a tournament organiser
    I need to be able to add scoring categories to a tournament

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "darkness"
        When I press "Login"
        Then I should be on "/"

    Scenario Outline: Set up some score for a tournament via the API
        Given I POST "<value>" to "/setTournamentScore" from the API
        Then the API response status code should be <code>
        Examples:
            |code | value          |
            |400  | foo            |
            |400  |                |
            |400  | key=sports     |
            |400  | tournamentId=northcon_2095 |
            |400  | minVal=2&maxVal=4 |
            |400  | tournamentId=northcon_1095&key=sports2&minVal=2&maxVal=4 |
            |200  | tournamentId=northcon_2095&key=sports |
            |200  | tournamentId=northcon_2095&key=sports2&minVal=2&maxVal=4 |
            |200  | tournamentId=northcon_2095&key=sports3&minVal=2 |
            |200  | tournamentId=northcon_2095&key=sports4&maxVal=4 |
