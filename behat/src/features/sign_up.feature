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
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password123"
        When I press "signup"
        When I wait for the response
        Then I should see "Account created"
        # TODO check that the fields are cleared
  
    @javascript
    Scenario: I sign up with an existing username
        Given I am on "/signup"
        When I fill in "inputUsername" with "Jerry"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password123"
        When I press "signup"
        When I wait for the response
        Then I should see "A user with the username Jerry already exists! Please choose another name"

    @javascript
    Scenario: I sign up with an existing password
        Given I am on "/signup"
        When I fill in "inputUsername" with "Gergich"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password123"
        When I press "signup"
        When I wait for the response
        Then I should see "Account created"

    @javascript
    Scenario: I miss all the fields
        Given I am on "/signup"
        When I press "signup"
        When I wait for the response
        Then I should see "Please fill in the required fields"

    @javascript
    Scenario Outline: I miss some fields
        Given I am on "/signup"
        When I fill in "inputUsername" with "Jimmy"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password123"
        When I fill in "<field>" with ""
        When I press "signup"
        When I wait for the response
        Then I should see "Please fill in the required fields"

        Examples:
            | field             |
            | inputUsername     |
            | inputEmail        |

    @javascript
    Scenario: I miss some passwords
        Given I am on "/signup"
        When I fill in "inputUsername" with "Jimmy"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with ""
        When I fill in "inputConfirmPassword" with "password123"
        When I press "signup"
        When I wait for the response
        Then I should see "Please enter two matching passwords"

    @javascript
    Scenario: I have different passwords
        Given I am on "/signup"
        When I fill in "inputUsername" with "Jimmy"
        When I fill in "inputEmail" with "foo@bar.com"
        When I fill in "inputPassword" with "password123"
        When I fill in "inputConfirmPassword" with "password1234"
        When I press "signup"
        When I wait for the response
        Then I should see "Please enter two matching passwords"



