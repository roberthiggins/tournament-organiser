Feature: Rank Entries Based on Scores
    I want to rank entries based on their scores for the tournament
    As a tournament organiser
    So I can give prizes appropriately

    @javascript
    Scenario: Bad targets
        Given I am on "/tournament/empty_tournament/rankings"
        Then I should see "There are no players entered for this event" appear

        Given I am on "/tournament/foo/rankings"
        Then I should see "Tournament foo not found in database" appear

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
