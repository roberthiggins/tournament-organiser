Feature: Enter a score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    # There are two ways to enter the score, using tournament id and player id
    # or by using the entry id directly

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "superman"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario: Logged in
        Given I am on "/enterscore/ranking_test/ranking_test_player_4"

    Scenario: Logged out
        Given I am on "/logout"
        Given I am on "/enterscore/ranking_test/ranking_test_player_4"
        Then I should be on "/login"

    Scenario: No permissions
        Given I am on "/logout"
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        Given I am on "/enterscore/painting_test/rick_james"
        When I select "Fanciness" from "id_key"
        When I fill in "id_value" with "1"
        Then I press "Enter Score"
        Then the response status code should be 200
        Then I should see "Permission denied"

    Scenario: A player not in the tournament
        Given I am on "/enterscore/painting_test/ranking_test_player_3"
        Then the response status code should be 404
        Then I should see "Entry for ranking_test_player_3 in tournament painting_test not found"

    Scenario Outline: I only know the tournament and username
        Given I am on "/enterscore/<tournament>/<username>"
        Then I should be on "<destination>"
        Then the response status code should be <code>
        Examples:
            |tournament         |username       |destination                    |code   |
            |                   |rick_james     |/enterscore//rick_james        |404    |
            |painting_test      |               |/enterscore/painting_test/     |404    |
            |foobar             |rick_james     |/enterscore/foobar/rick_james  |404    |
            |painting_test      |jimmy          |/enterscore/painting_test/jimmy|404    |

    @javascript
    Scenario Outline: I enter some scores
        Given I am on "/enterscore/painting_test/rick_james"
        When I wait for 1 second
        When I select "Fanciness" from "id_key"
        Then I fill in "id_value" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>"
        Examples:
            |score | content                                    |
            | 3    | Invalid score: 3                           |
            | 16   | Invalid score: 16                          |
            | 5    | Score entered for rick_james: 5            |
            | 6    | 6 not entered. Score is already set        |

    # TODO User controls
    Scenario: another player
        Given I am on "/logout"
        Given I am on "/enterscore/painting_test/stevemcqueen"
        When I fill in "id_inputUsername" with "rick_james"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        When I select "Fanciness" from "id_key"
        When I fill in "id_value" with "5"
        Then I press "Enter Score"
        Then the response status code should be 200
        Then I should see "Permission denied"

    Scenario: A non super user
        Given I am on "/logout"
        Given I am on "/enterscore/painting_test/stevemcqueen"
        When I fill in "id_inputUsername" with "stevemcqueen"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"
        When I select "Fanciness" from "id_key"
        When I fill in "id_value" with "5"
        Then I press "Enter Score"
        Then the response status code should be 200
        Then I should not see "Permission denied"
        Then I should see "Score entered for stevemcqueen: 5"
