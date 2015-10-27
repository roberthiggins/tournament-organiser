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
    Scenario: I create a valid tournament
        Given I am on "/createtournament"
        When I fill in "inputTournamentName" with "Red Harvest"
        When I press "Create"
        When I wait for the response
        Then I should see "Tournament created"

    @javascript
    Scenario: I fill in no fields
        Given I am on "/createtournament"
        When I press "Create"
        When I wait for the response
        Then I should see "Please fill in the required fields"

    @javascript
    Scenario Outline: I miss some fields
        Given I am on "/createtournament"
        When I fill in "inputTournamentName" with "Red Harvest"
        When I fill in "<field>" with ""
        When I press "Create"
        When I wait for the response
        Then I should see "Please fill in the required fields"

        Examples:
            | field                     |
            | inputTournamentName       |


