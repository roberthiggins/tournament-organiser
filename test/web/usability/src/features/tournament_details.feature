Feature: Get information about a tournament
    I want to get info about a tournament
    As a prospective player
    So that I can apply to the enter

    @javascript
    Scenario: Want info about painting_test
        Given I am on "/tournament/painting_test"
        Then I should see "Name: painting_test" appear
        Then I should see "Date: 2095-10-10" appear
        Then I should see "Apply to play in painting_test" appear

    @javascript
    Scenario: I try to visit a non-existent page
        Given I am on "/tournament/not_a_tournament"
        Then I should see "Tournament not_a_tournament not found" appear
