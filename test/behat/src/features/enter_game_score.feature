Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Enter a score for a round that's not ready
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should see "Next game not scheduled. Check with the TO." appear

    @javascript
    Scenario: Logged in
        When I am on "/tournament/enter_score_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "6"
        When I press "Set"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should see "Enter score for enter_score_test, Round 4" appear

    @javascript
    Scenario: Logged out
        Given I am on "/logout"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should be on "/login"

    @javascript
    Scenario: No permissions
        Given I am on "/logout"
        Given I am authenticated as "enter_score_test_player_2" using "password"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        When I wait for "Fair Play" to appear
        When I select "Fair Play" from "key"
        Then I fill in "value" with "5"
        Then I press "Enter Score"
        Then I should see "Permission denied" appear

    @javascript
    Scenario: A player not in the tournament
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_p_non/entergamescore"
        Then I should see "Unknown player: enter_score_test_p_non" appear

    @javascript
    Scenario Outline: I enter some scores
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        When I wait for "Fair Play" to appear
        When I select "Fair Play" from "key"
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>" appear
        Examples:
            |score | content                                            |
            | 0    | Invalid score: 0                                   |
            | 6    | Invalid score: 6                                   |
            | 5    | Score entered for enter_score_test_player_1: 5     |
            | 5    | 5 not entered. Score is already set                |

    @javascript
    Scenario: A regular user filling in their scores
        Given I am on "/logout"
        Given I am authenticated as "enter_score_test_player_4" using "password"
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_4/entergamescore"
        When I wait for "Fair Play" to appear
        When I select "Fair Play" from "key"
        Then I fill in "value" with "5"
        Then I press "Enter Score"
        Then I should see "Score entered for enter_score_test_player_4: 5" appear
