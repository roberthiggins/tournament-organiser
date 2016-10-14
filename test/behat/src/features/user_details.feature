Feature: See information about a user
    To know about my profile
    As a logged in user
    I need to be able to see the details on file about me

    @javascript
    Scenario Outline: See information about myself
        Given I am authenticated as "<user>" using "password"
        Given I am on "/user/ranking_test_player_1"
        Then I should see "User details for ranking_test_player_1:" appear
        Then I should see "Username: ranking_test_player_1" appear
        Then I should see "Email: ranking_test_player_1@bar.com" appear

        Examples:
            |user                  |
            |ranking_test_player_1 |
            |superman              |

    @javascript
    Scenario Outline: Auth
        Given I am authenticated as "<user>" using "password"
        Given I am on "/user/ranking_test_player_1"
        Then I should see "Permission denied for <user>" appear

        Examples:
            |user                  |
            |ranking_test_player_2 |
            |ranking_test_to       |
            |charlie_murphy        |
