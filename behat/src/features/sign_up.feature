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
            | username  |email        | password    | confirm     | response                            |
            | Jerry     |foo@bar.com  | password123 | password123 | Account created                     |
            | jerry     |foo@bar.com  | password123 | password123 | Account created                     |
            | jerry     |foo@bar.com  | password123 | password123 | Please choose another name          |
            # email is handled by django natively and is a hassle to check here
            |           |             |             |             | Enter the required fields           |
            |           |foo@bar.com  |             |             | Enter the required fields           |
            | good      |foo@bar.com  |             |             | Enter the required fields           |
# FIXME
            | good      |foo@bar.com  | password123 |             | Please enter two matching passwords |
            | good      |foo@bar.com  |             | password123 | Enter the required fields           |
            | mr        |foo@bar.com  | chulmondley | warner      | Please enter two matching passwords |
            | mr        |foo@bar.com  | password123 | password12  | Please enter two matching passwords |
            | mr        |foo@bar.com  | password123 | password1234| Please enter two matching passwords |
            | longymclongersone_who9foaiss8n |foo@bar.com  | password123 | password123 | Account created |

    Scenario: I want user details from the API
        When I GET "/userDetails/charlie_murphy" from the API
        Then the response is JSON
        Then the response has a "charlie_murphy" property

