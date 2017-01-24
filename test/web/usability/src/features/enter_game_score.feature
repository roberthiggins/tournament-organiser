Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Shows an error when there is something wrong with URL
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_p_non/entergamescore"
        Then I should see "Unknown player: enter_score_test_p_non" appear

    @javascript
    Scenario: Show message when URL correct
        Given I am on "/tournament/enter_score_test/entry/enter_score_test_player_5/entergamescore"
        Then I should see "Enter score for enter_score_test, Round 2" appear

    @javascript
    Scenario: See error
        When I am on "/tournament/enter_score_test/entry/enter_score_test_player_1/entergamescore"
        Then I should see "Next game not scheduled. Check with the TO." appear
        Then I should not see "Battle" appear
