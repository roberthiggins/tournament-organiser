Feature: Setup the scores a player can get in a tournament
    In order to let players get scores
    As a tournament organiser
    I need to be able to add scoring categories to a tournament

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario: I try to navigate to the page via the front page
        Given I am on "/devindex"
        When I follow "Setup Northcon_2095"
        Then I should be on "/tournamentsetup/northcon_2095"
        Then I should see "Score key"

    Scenario: I try to navigate to the page via URL
        Given I am on "/tournamentsetup/northcon_2095"
        Then I should see "Score key"

    Scenario: I try to navigate to the wrong URL
        Given I am on "/tournamentsetup/northcon_1095"
        Then the response status code should be 404

    Scenario Outline: Set up some score for a tournament via the web
        Given I am on "/tournamentsetup/southcon_2095"
        Then I fill in "id_key" with "<key>"
        When I select "some_category" from "scoreCategory"
        Then I press "Set Score"
        Then I should see "<response>"
        Examples:
            | key | response |
            | a   | Score created |
            | a   | Score already set |

    Scenario Outline: Set up some score for a tournament via the API
        Given I POST "<value>" to "/setTournamentScore" from the API
        Then the API response status code should be <code>
        Examples:
            |code | value          |
            |400  | foo            |
            |400  |                |
            |400  | key=sports     |
            |400  | tournamentId=northcon_2095 |
            |400  | tournamentId=northcon_2095&key=sports2 |
            |400  | tournamentId=northcon_1095&key=sports2&scoreCategory=100 |
            |200  | tournamentId=northcon_2095&key=sports&scoreCategory=100 |
            |200  | tournamentId=northcon_2095&key=sports2&scoreCategory=100|
