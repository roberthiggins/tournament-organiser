Feature: List Entries for a tournament
    I want to see all the people who have entered a tournament
    As a prospective player
    As this might influence my decision as to whether to enter

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "superman"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario: Visit the page from the front page
        Given I am on "/devindex"
        Then I follow "See entries for ranking_test"
        Then I am on "/ranking_test/entries"
        Then the response status code should be 200
        Then I should see "Entries:"
        Then I should see "homer"
        Then I should see "marge"
        Then I should see "lisa"
        Then I should see "bart"
        Then I should see "maggie"

    Scenario: A tournament with no entries
        Given I am on "/empty_tournament/entries"
        Then the response status code should be 200
        Then I should see "There are no entries yet. Be the first!"
        Then I follow "Be the first!"
        Then I am on "/registerforatournament"
        Then the response status code should be 200

    Scenario: Logged in user
        Then I am on "/ranking_test/entries"
        Then the response status code should be 200
        Then I should see "Entries:"
        Then I should see "homer"
        Then I should see "marge"
        Then I should see "lisa"
        Then I should see "bart"
        Then I should see "maggie"

    Scenario: A logged-out user
        Given I am on "/logout"
        Then I am on "/ranking_test/entries"
        Then I should be on "/login"

    Scenario: A non-existent tournament
        Given I am on "/not_a_thing/entries"
        Then the response status code should be 400
