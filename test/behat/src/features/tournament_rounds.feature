Feature: Set the number of rounds
    I want to see and change the number of rounds in a tournament
    As a TO
    So that the tournament can have more than one round

    Background:
        Given I am authenticated as "rounds_test_to" using "password"
        Given I am on "/tournament/rounds_test/rounds"
        When I wait for "Number of rounds" to appear

    @javascript
    Scenario: I change that number
        When I fill in "rounds" with "8"
        When I press "Set"
        Then I should see "Tournament rounds_test updated" appear
        Given I am on "/tournament/rounds_test/rounds"
        When I wait for "Number of rounds" to appear
        Then the "rounds" field should contain "8"

    @javascript
    Scenario Outline: Illegal values
        When I fill in "rounds" with "<val>"
        When I press "Set"
        Then I should see "<response>" appear

        Examples:
            | val | response                |
            | a   | Natural number required |
            | -1  | Natural number required |
            | 1.5 | Natural number required |
            | ''  | Natural number required |
