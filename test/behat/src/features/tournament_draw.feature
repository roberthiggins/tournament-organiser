Feature: Check the draw
    In order to see what game I need to play next
    As a player
    I want to be able to see the draw

    Background: Set the missions for a round robin tournament
        Given I POST "numRounds=4" to "/tournament/ranking_test/rounds" from the API
        Then the API response status code should be 200
        Then I POST "missions=[%22mission_1%22,%22mission_2%22,%22mission_3%22,%22%22]" to "/tournament/ranking_test/missions" from the API
        Then the API response status code should be 200

    @javascript
    Scenario Outline: Check the draw
        Given I am on "/tournament/<tournament>/round/<round>/draw"
        Then I should see "<text>" appear
        Examples:
            |tournament         | round | text                     |
            |foo                | 1     | Tournament foo not found |
            |foo                | 0     | Tournament foo not found |
            |                   |       |                          |
            |ranking_test       |       |                          |
            |                   | 1     |                          |
            |ranking_test       | 2     | mission_2                |
            |ranking_test       | 1     | mission_1                |
            |ranking_test       | 4     | TBA                      |
            |ranking_test       | 5     | Tournament ranking_test does not have a round 5|
            |mission_test       | 1     | No draw is available     |
