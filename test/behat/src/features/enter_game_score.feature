Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Logged out
        Given I am on "/logout"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should be on "/login"

    @javascript
    Scenario Outline: Bad targets
        Given I am on "/tournament/enter_score_test/entry/<user>/entergamescore"
        Then I should see "<result>" appear

        Examples:
            | user                      | result                                      |
            | enter_score_test_player_1 | Next game not scheduled. Check with the TO. |
            | enter_score_test_p_non    | Unknown player: enter_score_test_p_non      |

    @javascript
    Scenario: Logged in
        When I am on "/tournament/enter_score_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "6"
        When I press "Set"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should see "Enter score for enter_score_test, Round 4" appear

    @javascript
    Scenario Outline: I enter some scores
        Given I am authenticated as "<auth>" using "password"
        Given I am on "/tournament/enter_score_test/entry/<user>/entergamescore"
        When I wait for "Fair Play" to appear
        When I select "Fair Play" from "key"
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>" appear
        Examples:
            | auth                      |user                       | score | content                                        |
            | enter_score_test_player_2 | enter_score_test_player_1 |  5    | Permission denied                              |
            | enter_score_test_player_1 | enter_score_test_player_1 |  0    | Invalid score: 0                               |
            | enter_score_test_player_1 | enter_score_test_player_1 |  5    | Score entered for enter_score_test_player_1: 5 |
            | enter_score_test_player_1 | enter_score_test_player_1 |  5    | 5 not entered. Score is already set            |
