Feature: Check the draw
    In order to see what game I need to play next
    As a player
    I want to be able to see the draw

    Background: Set the missions for a round robin tournament
        Given I am authenticated as "superman" using "password"

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
            |ranking_test       | 1     | Kill                     |
            |ranking_test       | 2     | TBA                      |
            |ranking_test       | 3     | Tournament ranking_test does not have a round 3|
            |mission_test       | 1     | No draw is available     |
