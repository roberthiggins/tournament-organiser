Feature: Enter a tournament score for a player
    In order to get points in a tournament
    As a logged in user
    I want to enter scores

    @javascript
    Scenario Outline: I see some messages when I enter scores
        Given I am authenticated as "<auth>" using "password"
        Given I am on "/tournament/tourn_score_test/entry/stevemcqueen/enterscore"
        When I wait for "Fanciness" to appear
        Then I fill in "Fanciness" with "<score>"
        Then I press "Enter Score"
        Then I should see "<content>" appear
        Examples:
            | auth         | score | content                            |
            | rick_james   | 3     | Permission denied                  |
            | stevemcqueen | 5     | Score entered for stevemcqueen: 5  |
