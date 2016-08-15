Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    # There are two ways to enter the score, using tournament id and player id
    # or by using the entry id directly

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Logged in
        Given I am on "/enterscore/ranking_test/ranking_test_player_4"

    @javascript
    Scenario: Logged out
        Given I am on "/logout"
        Given I am on "/enterscore/ranking_test/ranking_test_player_4"
        Then I should be on "/login"

    @javascript
    Scenario: No permissions
        Given I am on "/logout"
        Given I am authenticated as "charlie_murphy" using "password"
        Given I am on "/enterscore/painting_test/rick_james"
        When I wait for "Enter score for rick_james" to appear
        When I select "Fanciness" from "key"
        When I fill in "value" with "1"
        Then I press "Enter Score"
        Then I should see "Permission denied" appear

    @javascript
    Scenario: A player not in the tournament
        Given I am on "/enterscore/painting_test/ranking_test_player_3"
        Then I should see "Entry for ranking_test_player_3 in tournament painting_test not found" appear

    @javascript
    Scenario Outline: I only know the tournament and username
        Given I am on "/enterscore/<tournament>/<username>"
        Then I should be on "<destination>"
        Then I should see "<code>" appear
        Examples:
            |tournament    |username   |destination                    |code            |
            |              |rick_james |/enterscore//rick_james        |Not Found       |
            |painting_test |           |/enterscore/painting_test/     |Not Found       |
            |painting_test |jimmy      |/tournament/painting_test/entry/jimmy/enterscore|Unknown player  |

    @javascript
    Scenario Outline: I enter some scores
        Given I am on "/enterscore/painting_test/rick_james"
        When I wait for "Enter score for rick_james" to appear
        When I select "Fanciness" from "key"
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>" appear
        Examples:
            |score | content                                    |
            | 3    | Invalid score: 3                           |
            | 16   | Invalid score: 16                          |
            | 5    | Score entered for rick_james: 5            |
            | 6    | 6 not entered. Score is already set        |

    @javascript
    Scenario: another player
        Given I am on "/logout"
        Given I am authenticated as "rick_james" using "password"
        Given I am on "/enterscore/painting_test/stevemcqueen"
        When I wait for "Enter score for stevemcqueen" to appear
        When I select "Fanciness" from "key"
        When I fill in "value" with "5"
        Then I press "Enter Score"
        Then I should see "Permission denied" appear

    @javascript
    Scenario: A non super user
        Given I am on "/logout"
        Given I am authenticated as "stevemcqueen" using "password"
        Given I am on "/enterscore/painting_test/stevemcqueen"
        When I wait for "Enter score for stevemcqueen" to appear
        When I select "Fanciness" from "key"
        When I fill in "value" with "5"
        Then I press "Enter Score"
        Then I should see "Score entered for stevemcqueen: 5" appear
