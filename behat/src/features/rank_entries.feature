Feature: Rank Entries Based on Scores
    I want to rank entries based on their scores for the tournament
    As a tournament organiser
    So I can give prizes appropriately

    Scenario: I get a rankings when no scores have been entered
    Scenario: I get rankings when scores have been entered
    Scenario: I get rankings for a tournament that doesn't exist
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

