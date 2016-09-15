Feature: Get the next game for a player
    When I need to get to a game
    As a logged in user
    I want to see the next game for a user (likely me)

    Background:
        Given I am authenticated as "superman" using "password"
        When I am on "/tournament/next_game_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "5"
        When I press "Set"

    @javascript
    Scenario: Check next game
        When I am on "/tournament/next_game_test/entry/next_game_test_player_1/nextgame"
        Then I should see "Retrieving info for your next game..."
        Then I should see "Next Game Info for next_game_test_player_1" appear
        Then I should see "Round: 4" appear
        Then I should see "Table: 3" appear
        Then I should see "Opponent: next_game_test_player_4" appear
        Then I should see "Mission: TBA" appear

    @javascript
    Scenario: Round that's not ready
        When I am on "/tournament/next_game_test/rounds"
        Then I should see "Number of rounds" appear
        When I fill in "rounds" with "2"
        When I press "Set"
        When I am on "/tournament/next_game_test/entry/next_game_test_player_1/nextgame"
        Then I should see "Retrieving info for your next game..."
        Then I should see "Next game not scheduled. Check with the TO." appear

    @javascript
    Scenario: Tournament that doesn't exist
        When I am on "/tournament/foo/entry/next_game_test_player_1/nextgame"
        Then I should see "Retrieving info for your next game..."
        Then I should see "Tournament foo doesn't exist" appear

    @javascript
    Scenario: Wrong player
        When I am on "/tournament/next_game_test/entry/ranking_test_player_1/nextgame"
        Then I should see "Retrieving info for your next game..."
        Then I should see "Entry for ranking_test_player_1 in tournament next_game_test not found" appear

    @javascript
    Scenario: Non-existent player
        When I am on "/tournament/next_game_test/entry/noone/nextgame"
        Then I should see "Retrieving info for your next game..."
        Then I should see "Unknown player: noone" appear

    @javascript
    Scenario: Logged out
        When I am on "/logout"
        When I am on "/tournament/next_game_test/entry/next_game_test_player_1/nextgame"
        Then I should be on "/login"
