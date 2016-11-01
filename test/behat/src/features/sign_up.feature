Feature: Sign up
    In order to use TO
    As any user
    I need to be able to sign up

    @javascript
    Scenario Outline: I try to navigate to the sign up page via a button
        Given I am on "/<base>"
        When I wait for "<button>" to appear
        When I follow "<button>"
        Then I should be on "/signup"
        Examples:
            | base  |button         |
            |       |Sign up        |
            | login |Create Account |

    @javascript
    Scenario Outline: I sign up with some new usernames
        Given I sign up "<username>"

        Examples:
            | username                       |
            | Jerry                          |
            | jerry                          |
            | longymclongersone_who9foaiss8n |

    @javascript
    Scenario Outline: I sign up incorrectly
        Given I am on "/signup"
        When I wait for "Username" to appear
        When I fill in "username" with "<user>"
        When I fill in "email" with "<email>"
        When I fill in "password1" with "<pword>"
        When I fill in "password2" with "<confirm>"
        When I press "Sign Up"
        Then I should see "<response>" appear

        Examples:
            | user  |email  | pword    | confirm   | response                                      |
            | jerry |a@b.c  | pword123 | pword123  | A user with the username jerry already exists |
            | jerry |       | pword123 | pword123  | This email does not appear valid              |
            |       |       |          |           | Please enter a username                       |
            |       |a@b.c  |          |           | Please enter a username                       |
            | good  |a@b.c  |          |           | Please enter two matching passwords           |
            | good  |a@b.c  | pword123 |           | Please enter two matching passwords           |
            | good  |a@b.c  |          | pword123  | Please enter two matching passwords           |
            | mr    |a@b.c  | pword123 | pword12   | Please enter two matching passwords           |
            | mr    |a@b.c  | pword123 | pword1234 | Please enter two matching passwords           |
