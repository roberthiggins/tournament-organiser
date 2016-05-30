Feature: Create a Tournament
    In order to run a tournament with TO players
    As a organiser
    I need to be able to create a tournament

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario: I try to navigate to the page via the front page
        Given I am on "/devindex"
        When I follow "Create a Tournament"
        Then I should see "add a tournament here"
        Then I should see "Name"
        #TODO All the other fields

    Scenario: I try to navigate to the page via the URL
        Given I am on "/createtournament"
        Then I should see "add a tournament here"
        Then I should see "Name"

    Scenario Outline: Valid and invalid values
        Given I am on "/createtournament"
        When I fill in "id_inputTournamentName" with "<name>"
        When I fill in "id_inputTournamentDate" with "<date>"
        When I press "Create"
        Then I should see "<response>"

        Examples:
            | name              | date          | response                      |
            |                   |               | This field is required        |
            | Red Harvest       |               | This field is required        |
            |                   | 2095-01-01    | This field is required        |
            | Red Harvest       | 2095-01-011   | Enter a valid date            |
            | Red Harvest       | 2095-13-01    | Enter a valid date            |
            | Red Harvest       | Red Harvest   | Enter a valid date            |
            | Red Harvest       | 2095-01-01    | Tournament created            |
            | Red Harvest       | 2096-01-01    | A tournament with name Red Harvest already exists     |

