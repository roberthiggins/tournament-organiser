Feature: Withdraw from a tournament
    I want to be able to withdraw from a tournament
    As someone with an application
    So that I don't have to play if something comes up

    @javascript
    Scenario: Withdraw a player
        Given I am authenticated as "withdrawal_test_2_p_1" using "password"

        Given I am on "/tournament/withdrawal_test_2"
        Then I should see "Entries:" appear
        Then I should see "Withdraw from withdrawal_test_2" appear
        When I press "Withdraw from withdrawal_test_2"
        Then I should see "Entry to withdrawal_test_2 withdrawn successfully" appear

        Given I am on "/tournament/withdrawal_test_2"
        Then I should see "Apply to play in withdrawal_test_2" appear

    @javascript
    Scenario: Withdraw, re-apply
        Given I am authenticated as "withdrawal_test_2_p_2" using "password"

        Given I am on "/tournament/withdrawal_test_2"
        Then I should see "Withdraw from withdrawal_test_2" appear
        When I press "Withdraw from withdrawal_test_2"
        Then I should see "Entry to withdrawal_test_2 withdrawn successfully" appear

        Given I am on "/tournament/withdrawal_test_2"
        Then I should see "Apply to play in withdrawal_test_2" appear
        When I press "Apply to play in withdrawal_test_2"
        Then I should see "Application Submitted" appear
