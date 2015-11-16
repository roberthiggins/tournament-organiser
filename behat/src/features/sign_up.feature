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
    Scenario Outline: I sign up with some new usernames
        Given I am on "/signup"
        When I fill in "inputUsername" with "<username>"
        When I fill in "inputEmail" with "<email>"
        When I fill in "inputPassword" with "<password>"
        When I fill in "inputConfirmPassword" with "<confirm>"
        When I press "signup"
        When I wait for the response
        Then I should see "<response>"
        # TODO check that the fields are cleared

        Examples:
            | username  |email        | password    | confirm     | response                            |
            | Jerry     |foo@bar.com  | password123 | password123 | Account created                     |
            | jerry     |foo@bar.com  | password123 | password123 | Account created                     |
            | jerry     |foo@bar.com  | password123 | password123 | Please choose another name          |
            | good      |@bar.com     | password123 | password123 | This email does not appear valid    |
            |           |             |             |             | Please fill in the required fields  |
            |           |foo@bar.com  |             |             | Please fill in the required fields  |
            | good      |foo@bar.com  |             |             | Please enter two matching passwords |
            | good      |foo@bar.com  | password123 |             | Please enter two matching passwords |
            | good      |foo@bar.com  |             | password123 | Please enter two matching passwords |
            | mr        |foo@bar.com  | chulmondley | warner      | Please enter two matching passwords |
            | mr        |foo@bar.com  | password123 | password12  | Please enter two matching passwords |
            | mr        |foo@bar.com  | password123 | password1234| Please enter two matching passwords |
            | longymclongersone_who9foaiss8n'sosif.asofadofh-asgy0ytn3gt |foo@bar.com  | password123 | password123 | Account created |

