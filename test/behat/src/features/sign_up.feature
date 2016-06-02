Feature: Sign up
    In order to use TO
    As any user
    I need to be able to sign up

    Scenario Outline: I try to navigate to the sign up page via a button
        Given I am on "/<base>"
        When I follow "<button>"
        Then I should see "Username"
        Then I should see "Email"
        Then I should see "Password"
        Then I should see "Password confirmation"
        Examples:
            |base       |button         |
            |           |Sign Up        |
            |login      |Create Account |

    Scenario: I try to navigate to the sign up page via url
        Given I am on "/signup"
        Then I should see "Username"
        Then I should see "Email"
        Then I should see "Password"
        Then I should see "Password confirmation"

    Scenario Outline: I sign up with some new usernames
        Given I am on "/signup"
        When I fill in "username" with "<username>"
        When I fill in "email" with "<email>"
        When I fill in "password1" with "<password>"
        When I fill in "password2" with "<confirm>"
        When I press "Sign Up"
        Then I should see "<response>"
        # TODO check that the fields are cleared

        Examples:
            | username  |email        | password    | confirm     | response                                    |
            | Jerry     |foo@bar.com  | password123 | password123 | Account created                             |
            | jerry     |foo@bar.com  | password123 | password123 | Account created                             |
            | jerry     |foo@bar.com  | password123 | password123 | A user with that username already exists    |
            # email is handled by django natively and is a hassle to check here
            |           |             |             |             | This field is required                      |
            |           |foo@bar.com  |             |             | This field is required                      |
            | good      |foo@bar.com  |             |             | This field is required                      |
            # FIXME
            | good      |foo@bar.com  | password123 |             | This field is required                      |
            | good      |foo@bar.com  |             | password123 | This field is required                      |
            | mr        |foo@bar.com  | chulmondley | warner      | The two password fields didn't match        |
            | mr        |foo@bar.com  | password123 | password12  | The two password fields didn't match        |
            | mr        |foo@bar.com  | password123 | password1234| The two password fields didn't match        |
            | longymclongersone_who9foaiss8n |foo@bar.com  | password123 | password123 | Account created        |
