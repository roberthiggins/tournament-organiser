Feature: Register for a Tournament
    In order to play competitive games
    As an account holder
    I need to be able to sign up to a tournament

    Background:
        Given I am authenticated as "register_test_player_1" using "password"

    @javascript
    Scenario: I visit the register page from the front page
        Given I am on "/"
        When I wait for "See upcoming tournaments" to appear
        When I follow "See upcoming tournaments"
        Then I should see "register_test_1 - 2222-06-01" appear
        When I follow "register_test_1 - 2222-06-01"
        Then I should see "Apply to play in register_test_1" appear

    @javascript
    Scenario: I visit the register page via the URL
        Given I am on "/tournament/register_test_1"
        Then I should see "Apply to play in register_test_1" appear

    @javascript
    Scenario Outline: I try to apply
        Given I am on "/tournament/<tournament>"
        When I wait for "Apply to play in <tournament>" to appear
        When I press "Apply to play in <tournament>"
        Then I should see "<response>" appear
        Given I am on "/tournament/<tournament>/entries"
        Then I should see "register_test_player_1" appear

        Examples:
            | tournament      | response                                     |
            | register_test_1 | Application submitted                        |
            | register_test_2 | Application submitted                        |
            | register_test_1 | You've already applied to register_test_1    |

    @javascript
    Scenario: I try to apply to a clashing tournament
        Given I am on "/tournament/register_test_3"
        When I wait for "Apply to play in register_test_3" to appear
        When I press "Apply to play in register_test_3"
        Then I should see "register_test_3 clashes with register_test_2" appear
