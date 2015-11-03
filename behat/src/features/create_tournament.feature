Feature: Create a Tournament
    In order to run a tournament with TO players
    As a organiser
    I need to be able to create a tournament

    Scenario: I try to navigate to the page via the front page
        Given I am on "/"
        When I follow "Create a Tournament"
        Then I should see "add a tournament here"
        Then I should see "Name"
        #TODO All the other fields

    Scenario: I try to navigate to the page via the URL
        Given I am on "/createtournament"
        Then I should see "add a tournament here"
        Then I should see "Name"

    @javascript
    Scenario Outline: Valid and invalid values
        Given I am on "/createtournament"
        When I fill in "inputTournamentName" with "<name>"
        When I fill in "inputTournamentDate" with "<date>"
        When I press "Create"
        When I wait for the response
        Then I should see "<response>"

        Examples:
            | name              | date          | response                                              |
            |                   |               | Please fill in the required fields                    |
            | Red Harvest       |               | Please fill in the required fields                    |
            |                   | 2095-01-01    | Please fill in the required fields                    |
            | Red Harvest       | 2095-01-011   | Enter a valid date                                    |
            | Red Harvest       | 2095-13-01    | Enter a valid date                                    |
            | Red Harvest       | Red Harvest   | Enter a valid date                                    |
            | Red Harvest       | 2095-01-01    | Tournament created                                    |
            | Red Harvest       | 2096-01-01    | A tournament with name Red Harvest already exists     |

