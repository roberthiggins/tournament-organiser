Feature: Set the number of rounds
    I want to see and change the number of rounds in a tournament
    As a TO
    So that the tournament can have more than one round

    Background:
        Given I am authenticated as "rounds_test_to" using "password"
        Given I am on "/tournament/rounds_test/rounds"
        When I wait for "Number of rounds" to appear

    @javascript
    Scenario Outline: I see some messages
        When I fill in "rounds" with "<num>"
        When I press "Set"
        Then I should see "<message>" appear
        Examples:
            | num | message                        |
            | a   | Natural number required        |
            | 8   | Tournament rounds_test updated |
