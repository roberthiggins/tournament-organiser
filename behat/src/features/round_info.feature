Feature: Get round info for display to the user
    I want to be able to get information on a single round in a tournament
    As a tournament entrant
    So that I can know about scores, mission, etc.

    Scenario: I get round info from the API
        When I GET "/roundInfo/ranking_test/1" from the API
        Then the response is JSON
        Then the API response should contain "round_1_battle"
        Then the API response should contain "Kill"
        Then the API response should not contain "round_2_battle"
        Then the API response should not contain "sports"

    Scenario Outline: I send malformed data
        When I GET "/roundInfo/<tourn>/<round>" from the API
        Then the API response status code should be <code>

        Examples:
            |tourn              | round         | code  |
            | foo               | 1             | 400   |
            | ranking_test      | 4             | 400   |
            | 1                 | ranking_test  | 400   |
            | 1                 | 1             | 400   |
            | ranking_test      | -1            | 400   |
            | ranking_test      | ranking_test  | 400   |
