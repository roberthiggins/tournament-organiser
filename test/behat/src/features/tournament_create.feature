Feature: Create a Tournament
    In order to run a tournament with TO players
    As a organiser
    I need to be able to create a tournament

    Background:
        Given I am authenticated as "charlie_murphy" using "password"

    @javascript
    Scenario: I try to navigate to the page via the front page
        Given I am on "/devindex"
        When I wait for "Create a Tournament" to appear
        When I follow "Create a Tournament"
        Then I should see "add a tournament here" appear
        Then I should see "Name" appear

    @javascript
    Scenario: I try to navigate to the page via the URL
        Given I am on "/createtournament"
        Then I should see "You can add a tournament here" appear
        Then I should see "Tournament Name" appear
        Then I should see "Tournament Date" appear

    @javascript
    Scenario Outline: Valid and invalid values
        Given I am on "/createtournament"
        When I wait for "You can add a tournament here" to appear
        When I fill in "name" with "<name>"
        When I fill in "date" with "<date>"
        When I press "Create"
        Then I should see "<response>" appear

        Examples:
            | name              | date          | response                      |
            |                   |               | Enter a valid                 |
            | Red Harvest       |               | Enter a valid date            |
            |                   | 2095-01-01    | Enter a valid name            |
            | Red Harvest       | 2095-13-01    | Enter a valid date            |
            | Red Harvest       | Red Harvest   | Enter a valid date            |
            | Red Harvest       | 2095-01-01    | Tournament created            |
            | Red Harvest       | 2096-01-01    | A tournament with name Red Harvest already exists     |

