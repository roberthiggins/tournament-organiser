Feature: Get the next game for a player
    When I need to get to a game
    As a logged in user
    I want to see the next game for a user (likely me)

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Check next game for next_game_test_player_5
        When I am on "/tournament/next_game_test/entry/next_game_test_player_5/nextgame"
        Then I should see "Next Game Info for next_game_test_player_5" appear
        Then I should see "Round: 2" appear
        Then I should see "Table: 2" appear
        Then I should see "Opponent: next_game_test_player_4" appear
        Then I should see "Mission: TBA" appear

    @javascript
    Scenario: See error
        When I am on "/tournament/next_game_test/entry/next_game_test_player_1/nextgame"
        Then I should see "Next game not scheduled. Check with the TO." appear
