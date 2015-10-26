Feature: Sign up
    In order to use TO
    As any user
    I need to be able to sign up

    Scenario: I try to navigate to the sign up page via a button
        Given I am on "/"
        When I follow "Sign Up"
        Then I should see "User Name"
        Then I should see "Email Address"
        Then I should see "Password"
        Then I should see "Confirm Password"

    Scenario: I try to navigate to the sign up page via url
        Given I am on "/signup"
        Then I should see "User Name"
        Then I should see "Email Address"
        Then I should see "Password"
        Then I should see "Confirm Password"

    @javascript
    Scenario: I sign up with a new username
        Given I am on "/signup"
        When I fill in "inputUsername" with "Jerry"
        When I fill in "inputEmail" with "Gergich"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password123"
        When I press "signup"
        When I wait for the response
        Then I should see "Account created"
        # TODO check that the fields are cleared
  
    Scenario: I sign up with an existing username
    Scenario: I sign up with an existing password
    Scenario: I miss all the fields
    Scenario: I miss the username field
    Scenario: I miss the email field
    Scenario: I miss the password field
    Scenario: I miss the confirm password field
    Scenario: I have different passwords

