Feature: Sign up
    In order to use TO
    As any user
    I need to be able to sign up

    @javascript
    Scenario: I try to navigate to the sign up page via a button
        Given I am on "/"
        When I wait for "Sign up" to appear
        When I follow "Sign up"
        Then I should be on "/signup"

    @javascript
    Scenario Outline: I see some messages when I try to sign up
        Given I am on "/signup"
        When I wait for "Username" to appear
        When I fill in "username" with "<user>"
        When I fill in "email" with "<email>"
        When I fill in "password1" with "<pword>"
        When I fill in "password2" with "<confirm>"
        When I press "Sign Up"
        Then I should see "<response>" appear

        Examples:
            | user       |email | pword    | confirm  | response |
            | su_test_3  |a@b.c | password | password | Account Created |
            | su_test_3  |a@b.c | password | password | A user with the username su_test_3 already exists |
