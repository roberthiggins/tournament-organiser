Feature: List Entries for a tournament
    I want to see all the people who have entered a tournament
    As a prospective player
    As this might influence my decision as to whether to enter

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Visit the page from the front page
        Given I am on "/devindex"
        When I wait for "See entries for ranking_test" to appear
        Then I follow "See entries for ranking_test"
        Then I am on "/tournament/ranking_test/entries"
        Then I should see "Entries:" appear
        Then I should see "ranking_test_player_1" appear
        Then I should see "ranking_test_player_2" appear
        Then I should see "ranking_test_player_3" appear
        Then I should see "ranking_test_player_4" appear
        Then I should see "ranking_test_player_5" appear

    @javascript
    Scenario: A tournament with no entries
        Given I am on "/tournament/empty_tournament/entries"
        Then I should see "There are no entries yet. Be the first!" appear
        Then I follow "Be the first!"
        Then I am on "/tournament/empty_tournament/register"

    @javascript
    Scenario: Logged in user
        Then I am on "/tournament/ranking_test/entries"
        Then I should see "Entries:" appear
        Then I should see "ranking_test_player_1" appear
        Then I should see "ranking_test_player_2" appear
        Then I should see "ranking_test_player_3" appear
        Then I should see "ranking_test_player_4" appear
        Then I should see "ranking_test_player_5" appear

    @javascript
    Scenario: A logged-out user
        Given I am on "/logout"
        Then I am on "/tournament/ranking_test/entries"
        Then I should be on "/login"

    @javascript
    Scenario: A non-existent tournament
        Given I am on "/tournament/not_a_thing/entries"
        Then I should see "Tournament not_a_thing doesn't exist" appear
