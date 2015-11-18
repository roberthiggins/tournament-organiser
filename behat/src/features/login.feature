Feature: Login
    I want to be able to log in
    As an account holder
    So I can access data specific to me

    Background:
        Given I am on "/signup"
        When I fill in "username" with "testuser"
        When I fill in "email" with "foo@bar.com"
        When I fill in "password1" with "shazam"
        When I fill in "password2" with "shazam"
        When I press "signup"

    Scenario: I Want to go to the login page
        Given I am on "/"
        When I follow "Login"
        Then I should see "Username"
        Then I should see "Password"
        Then I should see "Forgot Password"

        Given I am on "/login"
        Then I should see "Username"
        Then I should see "Password"
        Then I should see "Forgot Password"

    Scenario: I log in with correct details
        Given I am on "/login"
        When I fill in "id_inputUsername" with "testuser"
        When I fill in "id_inputPassword" with "shazam"
        When I press "Login"
        Then I should be on "/login"

    Scenario Outline: I try to log in
        Given I am on "/login"
        When I fill in "id_inputUsername" with "<uname>"
        When I fill in "id_inputPassword" with "<password>"
        When I press "Login"
        Then I should be on "/login"
        Then I should see "<response>"

        Examples:
            |uname              |password       |response                       |
            |foo                |               |This field is required         |
            |                   |bar            |This field is required         |
            |                   |               |This field is required         |
            |steveqmcqueen      |password12     |Username or password incorrect |
            |steveqmcqueenie    |password123    |Username or password incorrect |

