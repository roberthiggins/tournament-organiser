Feature: Sign up
    In order to use TO
    As any user
    I need to be able to sign up

    @javascript
    Scenario Outline: I try to navigate to the sign up page via a button
        Given I am on "/<base>"
        When I wait for "<button>" to appear
        When I follow "<button>"
        Then I should see "Username" appear
        Then I should see "Email" appear
        Then I should see "Password" appear
        Then I should see "Password confirmation" appear
        Examples:
            | base  |button         |
            |       |Sign up        |
            | login |Create Account |

    @javascript
    Scenario: I try to navigate to the sign up page via url
        Given I am on "/signup"
        Then I should see "Username" appear
        Then I should see "Email" appear
        Then I should see "Password" appear
        Then I should see "Password confirmation" appear

    @javascript
    Scenario Outline: I sign up with some new usernames
        Given I am on "/signup"
        When I wait for "Username" to appear
        When I fill in "username" with "<username>"
        When I fill in "email" with "<email>"
        When I fill in "password1" with "<password>"
        When I fill in "password2" with "<confirm>"
        When I press "Sign Up"
        Then I should see "<response>" appear
        # TODO check that the fields are cleared

        Examples:
            | username  |email        | password    | confirm     | response                                    |
            | Jerry     |foo@bar.com  | password123 | password123 | Account created                             |
            | jerry     |foo@bar.com  | password123 | password123 | Account created                             |
            | jerry     |foo@bar.com  | password123 | password123 | A user with the username jerry already exists    |
            | jerry     |             | password123 | password123 | This email does not appear valid            |
            |           |             |             |             | Please enter a username                      |
            |           |foo@bar.com  |             |             | Please enter a username                      |
            | good      |foo@bar.com  |             |             | Please enter two matching passwords         |
            | good      |foo@bar.com  | password123 |             | Please enter two matching passwords         |
            | good      |foo@bar.com  |             | password123 | Please enter two matching passwords         |
            | mr        |foo@bar.com  | chulmondley | warner      | Please enter two matching passwords         |
            | mr        |foo@bar.com  | password123 | password12  | Please enter two matching passwords         |
            | mr        |foo@bar.com  | password123 | password1234| Please enter two matching passwords         |
            | longymclongersone_who9foaiss8n |foo@bar.com  | password123 | password123 | Account created        |
