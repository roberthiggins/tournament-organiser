Feature: Enter a tournament score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    @javascript
    Scenario: Logged in
        Given I am on "/tournament/ranking_test/entry/ranking_test_player_4/enterscore"
        Then I should be on "/login"
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/ranking_test/entry/ranking_test_player_4/enterscore"
        Then I should be on "/tournament/ranking_test/entry/ranking_test_player_4/enterscore"

    @javascript
    Scenario Outline: Bad targets
        Given I am authenticated as "superman" using "password"
        Given I am on "/tournament/<tournament>/entry/<username>/enterscore"
        Then I should see "<code>" appear
        Examples:
            |tournament    |username              |code           |
            |              |rick_james            |Not Found      |
            |painting_test |                      |Not Found      |
            |painting_test |jimmy                 |Unknown player |
            |painting_test |ranking_test_player_3 |not found      |

    @javascript
    Scenario Outline: I enter some scores
        Given I am authenticated as "<auth>" using "password"
        Given I am on "/tournament/painting_test/entry/rick_james/enterscore"
        When I wait for "Enter score for rick_james" to appear
        When I select "Fanciness" from "key"
        Then I fill in "value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>" appear
        Examples:
            |auth           |score | content                                    |
            |charlie_murphy | 3    | Permission denied                           |
            |rick_james     | 3    | Invalid score: 3                           |
            |rick_james     | 16   | Invalid score: 16                          |
            |rick_james     | 5    | Score entered for rick_james: 5            |
            |rick_james     | 6    | 6 not entered. Score is already set        |
