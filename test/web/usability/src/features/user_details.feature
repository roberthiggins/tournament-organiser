Feature: See information about a user
    To know about my profile
    As a logged in user
    I need to be able to see the details on file about me

    @javascript
    Scenario Outline: See some messages
        Given I am authenticated as "<user>" using "password"
        Given I am on "/user/ranking_test_player_1"
        Then I should see "<message>" appear

        Examples:
            |user                  | message                                     |
            |ranking_test_player_1 | User details for ranking_test_player_1      |
            |ranking_test_player_2 | Permission denied for ranking_test_player_2 |
