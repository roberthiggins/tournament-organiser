Feature: Login
    I want to be able to log in
    As an account holder
    So I can access data specific to me

    Background:
        Given I am on "/signup"
        When I fill in "inputUsername" with "testuser"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "shazam"
        When I fill in "inputConfirmPassword" with "shazam"
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

    @javascript
    Scenario Outline: I try to log in
        Given I am on "/login"
        When I fill in "inputUsername" with "<uname>"
        When I fill in "inputPassword" with "<password>"
        When I press "Login"
        When I wait for the response
        Then I should see "<response>"

        Examples:
            |uname              |password       |response                       |
            |foo                |               |Enter username and password    |
            |                   |bar            |Enter username and password    |
            |                   |               |Enter username and password    |
            |steveqmcqueen      |password12     |Username or password incorrect |
            |steveqmcqueenie    |password123    |Username or password incorrect |
            |testuser           |shazam         |Login successful               |

