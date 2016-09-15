Feature: Set the number of rounds
    I want to see and change the number of rounds in a tournament
    As a TO
    So that the tournament can have more than one round

    Background: Login
        Given I am authenticated as "rounds_test_to" using "password"
        Given I am on "/tournament/rounds_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "5"
        When I press "Set"        

    @javascript
    Scenario: I check the number of rounds in a tournament
        Given I am on "/tournament/rounds_test/rounds"
        Then I should see "Number of rounds" appear
        Then the "rounds" field should contain "5"

    @javascript
    Scenario: I change that number
        Given I am on "/tournament/rounds_test/rounds"
        When I wait for "Number of rounds" to appear
        When I fill in "rounds" with "8"
        When I press "Set"

        Given I am on "/tournament/rounds_test/rounds"
        When I wait for "Number of rounds" to appear
        Then the "rounds" field should contain "8"
