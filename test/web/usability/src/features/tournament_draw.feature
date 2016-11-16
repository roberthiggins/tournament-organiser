Feature: Check the draw
    In order to see what game I need to play next
    As a player
    I want to be able to see the draw

    @javascript
    Scenario Outline: Check the draw
        Given I am on "/tournament/<tournament>/round/<round>/draw"
        Then I should see "<text>" appear
        Examples:
            |tournament   | round | text                           |
            |foo          | 1     | Tournament foo not found       |
            |ranking_test | 1     | Draw for Round 1, ranking_test |
