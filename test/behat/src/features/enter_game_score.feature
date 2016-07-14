Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "superman"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        When I am on "/setrounds/enter_score_test"
        When I fill in "numRounds" with "6"
        When I press "Set"

    Scenario: Logged in
        Given I am on "/entergamescore/enter_score_test/enter_score_test_player_1"

    Scenario: Logged out
        Given I am on "/logout"
        Given I am on "/entergamescore/enter_score_test/enter_score_test_player_1"
        Then I should be on "/login"

    Scenario: No permissions
        Given I am on "/logout"
        Given I am on "/login"
        When I fill in "id_inputUsername" with "enter_score_test_player_2"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        Given I am on "/entergamescore/enter_score_test/enter_score_test_player_1"
        When I select "Fair Play" from "id_key"
        Then I fill in "id_value" with "5"
        Then I press "Enter Score"
        Then the response status code should be 200
        Then I should see "Permission denied"

    Scenario: A player not in the tournament
        Given I am on "/entergamescore/enter_score_test/enter_score_test_p_non"
        Then the response status code should be 404
        Then I should see "Unknown player: enter_score_test_p_non"

    @javascript
    Scenario Outline: I enter some scores
        Given I am on "/entergamescore/enter_score_test/enter_score_test_player_1"
        When I wait for 1 second
        When I select "Fair Play" from "id_key"
        Then I fill in "id_value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>"
        Examples:
            |score | content                                            |
            | 0    | Invalid score: 0                                   |
            | 6    | Invalid score: 6                                   |
            | 5    | Score entered for enter_score_test_player_1: 5     |
            | 5    | 5 not entered. Score is already set                |

    Scenario: A regular user filling in their scores
        Given I am on "/logout"
        Given I am on "/entergamescore/enter_score_test/enter_score_test_player_4"
        When I fill in "id_inputUsername" with "enter_score_test_player_4"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        When I select "Fair Play" from "id_key"
        Then I fill in "id_value" with "5"
        Then I press "Enter Score"
        Then the response status code should be 200
        Then I should not see "Permission denied"
        Then I should see "Score entered for enter_score_test_player_4: 5"
