Feature: Login
    I want to be able to log in
    As an account holder
    So I can access data specific to me

    Background:
        Given I am on "/logout"

    @javascript
    Scenario: I Want to go to the login page
        Given I am on "/"
        When I wait for "Login" to appear
        When I follow "Login"
        Then I should see "Username" appear
        Then I should see "Password" appear
        Then I should see "Forgot Password" appear

        Given I am on "/login"
        Then I should see "Username" appear
        Then I should see "Password" appear
        Then I should see "Forgot Password" appear

    @javascript
    Scenario: I log in with correct details
        Given I am on "/login"
        When I wait for "Login to your account" to appear
        When I fill in "username" with "charlie_murphy"
        When I fill in "password" with "password"
        When I press "Login"
        Then I should see "Welcome to the Tournament Organiser" appear

    @javascript
    Scenario Outline: I try to log in
        Given I am on "/login"
        When I wait for "Login to your account" to appear
        When I fill in "username" with "<uname>"
        When I fill in "password" with "<password>"
        When I press "Login"
        Then I should be on "/login"
        Then I should see "<response>" appear

        Examples:
            |uname              |password       |response                       |
            |foo                |               |Missing credentials            |
            |                   |bar            |Missing credentials            |
            |                   |               |Missing credentials            |
            |steveqmcqueen      |password12     |Username or password incorrect |
            |steveqmcqueenie    |password123    |Username or password incorrect |

    @javascript
    Scenario: While logged in I try to log in again
        Given I am authenticated as "superman" using "password"
        Given I am on "/login"
        When I wait for "Login to your account" to appear
        When I fill in "username" with "charlie_murphy"
        When I fill in "password" with "password"
        When I press "Login"
        When I wait for "Welcome to the Tournament Organiser" to appear
        Then I should be on "/"
