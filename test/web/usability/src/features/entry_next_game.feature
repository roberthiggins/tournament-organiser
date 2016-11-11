Feature: Get the next game for a player
    When I need to get to a game
    As a logged in user
    I want to see the next game for a user (likely me)

    Background:
        Given I am authenticated as "superman" using "password"

    @javascript
    Scenario: Check next game
        When I am on "/tournament/next_game_test/entry/next_game_test_player_5/nextgame"
        Then I should see "Next Game Info for next_game_test_player_5" appear
        Then I should see "Round: 2" appear
        Then I should see "Table: 2" appear
        Then I should see "Opponent: next_game_test_player_4" appear
        Then I should see "Mission: TBA" appear

    @javascript
    Scenario Outline: Bad targets
        When I am on "/tournament/<tournament>/entry/<user>/nextgame"
        Then I should see "<result>" appear

        Examples:
            | tournament     | user                    | result                                                                 |
            | foo            | next_game_test_player_5 | Tournament foo doesn't exist                                           |
            | next_game_test | ranking_test_player_1   | Entry for ranking_test_player_1 in tournament next_game_test not found |
            | next_game_test | noone                   | Unknown player: noone                                                  |

    @javascript
    Scenario: Logged out
        When I am on "/logout"
        When I am on "/tournament/next_game_test/entry/next_game_test_player_5/nextgame"
        Then I should be on "/login"

    @javascript
    Scenario: Round that's not ready
        When I am on "/tournament/next_game_test/entry/next_game_test_player_1/nextgame"
        Then I should see "Next game not scheduled. Check with the TO." appear
