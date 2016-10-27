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
        Given I am on "/tournament/create"
        Then I should see "You can add a tournament here" appear
        Then I should see "Tournament Name:" appear
        Then I should see "Tournament Date:" appear
        Then I should see "Number of Rounds:" appear

    @javascript
    Scenario: I make a tournament using all the values
        Given I am on "/tournament/create"
        Then I should see "You can add a tournament here" appear
        When I fill in "name" with "test_tournament_creation"
        When I fill in "date" with "9999-12-31"
        When I fill in "rounds" with "1"
        When I fill category 0 with "foo" "10" "10" "10"
        When I fill category 1 with "bar" "10" "10" "10"
        When I press "Create"
        Then I should see "Tournament created!" appear
        Then I should see "Name: test_tournament_creation" appear
        Then I should see "Date: 9999-12-31" appear
        Then I should see "Rounds: 1" appear
        Then I should see "Score Categories: foo, bar" appear

    @javascript
    Scenario: I make a tournament using the minimum values
        Given I am on "/tournament/create"
        Then I should see "You can add a tournament here" appear
        When I fill in "name" with "test_tournament_creation_2"
        When I fill in "date" with "9999-12-31"
        When I fill in "rounds" with ""
        When I fill category 0 with "" "" "" ""
        When I press "Create"
        Then I should see "Tournament created!" appear
        Then I should see "Name: test_tournament_creation" appear
        Then I should see "Date: 9999-12-31" appear

    @javascript
    Scenario Outline: Valid and invalid values
        Given I am on "/tournament/create"
        When I wait for "You can add a tournament here" to appear
        When I fill in "name" with "<name>"
        When I fill in "date" with "<date>"
        When I press "Create"
        Then I should see "<response>" appear

        Examples:
            | name | date        | response            |
            |      |             | Enter a valid       |
            | red  |             | Enter a valid date  |
            |      | 2095-01-01  | Enter a valid name  |
            | red  | 2095-13-01  | Enter a valid date  |
            | red  | red         | Enter a valid date  |
            | red  | 2095-01-01  | Tournament created  |
            | red  | 2096-01-01  | A tournament with name red already exists |
