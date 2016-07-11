Feature: Rank Entries Based on Scores
    I want to rank entries based on their scores for the tournament
    As a tournament organiser
    So I can give prizes appropriately

    Scenario: Visit the page from the front page
        Given I am on "/devindex"
        Then I follow "See the current placings for ranking_test"
        Then I am on "/rankings/ranking_test"
        Then the response status code should be 200

    Scenario: I get a rankings when no scores have been entered
        Given I am on "/rankings/northcon_2095"
        Then the response status code should be 200
        Then I should see "There are no players entered for this event"
        Given I am on "/rankings/painting_test"
        Then the response status code should be 200
        Then I should see "rick_james"

    Scenario: I get rankings when scores have been entered
        Given I am on "/rankings/ranking_test"
        Then the response status code should be 200
        Then I should see "ranking_test_player_1"
        Then I should see "ranking_test_player_2"
        Then I should see "ranking_test_player_3"
        Then I should see "ranking_test_player_4"
        Then I should see "ranking_test_player_5"
        Then I should see "84.75"
        Then I should see "10.00"

    Scenario: I get rankings for a tournament that doesn't exist
        Given I am on "rankings/foo"
        Then the response status code should be 404

    # TODO
    Scenario: A member of the public wants to see protected scores
