Feature: Get information about an entry
    In order to enter scores for players
    As a user
    I want to be able to get basic information about an entry

    Scenario: Use the API to get information
        When I GET "/entryInfo/ranking_test/lisa" from the API
        Then the response is JSON

    Scenario Outline: Malformed
        When I GET "<value>" from the API
        Then the API response status code should be <code>
        Examples:
            | value             | code  |
            | /entryinfo/1      | 404   |
            | /entryInfo        | 404   |
            | /entryInfo/       | 404   |
            | /entryInfo/0      | 400   |
            | /entryInfo/1/     | 404   |
            | /entryInfo/a      | 400   |
      
