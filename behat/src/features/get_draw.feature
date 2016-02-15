Feature: Check the draw
    In order to see what game I need to play next
    As a player
    I want to be able to see the draw

    Scenario Outline: Check the draw
        Given I am on "/draw/<tournament>/<round>"
        Then I should see "<text>"
        Then the response status code should be <code>
        Examples:
            |tournament         | round | code   | text                         |
            |foo                | 1     | 200    | Tournament foo not found     |
            |foo                | 0     | 200    | Tournament foo not found     |
            |                   |       | 404    |                              |
            |                   | 1     | 404    |                              |
            |ranking_test       | 2     | 200    | lisa                         |
            |ranking_test       | 1     | 200    | lisa                         |
            |ranking_test       | 4     | 200    | Draw not ready. Mission not set. Contact TO   |
            |ranking_test       |       | 404    |                              |
