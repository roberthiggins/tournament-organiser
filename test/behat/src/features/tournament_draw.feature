Feature: Check the draw
    In order to see what game I need to play next
    As a player
    I want to be able to see the draw

    Background: Set the missions for a round robin tournament
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Setup not needed in the background
        When I am on "/tournament/ranking_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "4"
        When I press "Set"
        Given I am on "/tournament/ranking_test/missions"
        Then I wait for "Set the missions for ranking_test here" to appear
        When I fill in "missions_0" with "mission_1"
        When I fill in "missions_1" with "mission_2"
        When I fill in "missions_2" with "mission_3"
        When I press "Set"

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
