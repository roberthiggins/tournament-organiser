Feature: Modify a user's details
    When I change my email address or name
    As any user
    I need to be able to update my account

    @javascript
    Scenario Outline: I see some messages
        Given I am authenticated as "user_update_test" using "password"
        Given I am on "/user/user_update_test/update"
        Then I should see "You can add/change your details here" appear
        Then I should see "user_update_test@bar.com" appear in field "email"
        Then I fill in "first_name" with "<name>"
        Then I fill in "email" with "<email>"
        Then I press "Update"
        Then I should see "<message>" appear

        Examples:
            | name | email | message                          |
            | foo  | c.b@a | This email does not appear valid |
            | foo  | a@b.c | Account updated                  |
