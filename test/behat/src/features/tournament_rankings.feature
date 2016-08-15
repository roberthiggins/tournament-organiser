Feature: Rank Entries Based on Scores
    I want to rank entries based on their scores for the tournament
    As a tournament organiser
    So I can give prizes appropriately

    @javascript
    Scenario: Visit the page from the front page
        Given I am on "/devindex"
        When I wait for "See the current placings for ranking_test" to appear
        Then I follow "See the current placings for ranking_test"
        Then I am on "/tournament/ranking_test/rankings"
        Then I should see "Placings for ranking_test" appear

    @javascript
    Scenario: I get a rankings when no scores have been entered
        Given I am on "/tournament/northcon_2095/rankings"
        Then I should see "There are no players entered for this event" appear
        Given I am on "/tournament/painting_test/rankings"
        Then I should see "rick_james" appear

    @javascript
    Scenario: I get rankings when scores have been entered
        Given I am on "/tournament/ranking_test/rankings"
        Then I should see "ranking_test_player_1" appear
        Then I should see "ranking_test_player_2" appear
        Then I should see "ranking_test_player_3" appear
        Then I should see "ranking_test_player_4" appear
        Then I should see "ranking_test_player_5" appear
        Then I should see "84.75" appear
        Then I should see "10.00" appear

    @javascript
    Scenario: I get rankings for a tournament that doesn't exist
        Given I am on "/tournament/foo/rankings"
        Then I should see "Tournament foo doesn't exist" appear
