Feature: Rank Entries Based on Scores
    I want to rank entries based on their scores for the tournament
    As a tournament organiser
    So I can give prizes appropriately

    Scenario: Visit the page from the front page
        Given I am on "/"
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
        Then I should see "homer"
        Then I should see "marge"

    Scenario: I get rankings for a tournament that doesn't exist
        Given I am on "rankings/foo"
        Then the response status code should be 404

    # TODO
    Scenario: A member of the public wants to see protected scores

    # API
    Scenario: I get rankings when scores have been entered
        Given I GET "/rankEntries/ranking_test" from the API
        Then the API response status code should be 200
        Then the response is JSON
        Then the API response should contain "homer"
        Then the API response should contain "marge"

    Scenario: I get rankings for a tournament that doesn't exist
        Given I GET "/rankEntries/foo" from the API
        Then the API response status code should be 404

