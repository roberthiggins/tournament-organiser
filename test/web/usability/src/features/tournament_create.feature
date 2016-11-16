Feature: Create a Tournament
    In order to run a tournament with TO players
    As a organiser
    I need to be able to create a tournament

    Background:
        Given I am authenticated as "charlie_murphy" using "password"

    @javascript
    Scenario: I try to navigate to the page via the front page
        Given I am on "/"
        When I wait for "Create a Tournament" to appear
        When I follow "Create a Tournament"
        Then I should see "Create Tournament" appear
        Then I should see "Name" appear

    @javascript
    Scenario Outline: See some messages
        Given I visit the tournament creation page
        When I fill in "name" with "<name>"
        When I fill in "date" with "<date>"
        When I press "Create"
        Then I should see "<response>" appear

        Examples:
            | name | date        | response            |
            | red  | red         | Enter a valid date  |
            | red  | 2095-01-01  | Tournament created  |
