Feature: Login
    I want to be able to log in
    As an account holder
    So I can access data specific to me

    @javascript
    Scenario Outline: I log in with correct details
        Given I am on "/logout"
        Given I am on "/login"
        When I wait for "Login to your account" to appear
        When I fill in "username" with "<user>"
        When I fill in "password" with "<pass>"
        When I press "Login"
        Then I should see "<msg>" appear
        Then I should be on "<path>"
        Examples:
            |user     | pass     | path   | msg                       |
            |superman | password | /      | Welcome to the Tournament |
            |foo      |          | /login | Missing credentials       |
