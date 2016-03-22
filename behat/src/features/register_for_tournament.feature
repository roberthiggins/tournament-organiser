Feature: Register for a Tournament
    In order to play competitive games
    As an account holder
    I need to be able to sign up to a tournament

    Background:
        Given I am on "/login"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "password"
        When I press "Login"

    Scenario: I visit the register page from the front page
        Given I am on "/devindex"
        When I follow "Register for a Tournament"
        Then I should see "Select a tournament to register for"

    Scenario: I visit the register page via the URL
        Given I am on "/registerforatournament"
        Then I should see "Select a tournament to register for"

    Scenario: I use the API to list tournaments
        When I GET "/listtournaments" from the API
        Then the response is JSON
        Then the response has a "tournaments" property

    Scenario Outline: I miss some fields
        Given I am on "/registerforatournament"
        When I select "<tournament>" from "inputTournamentName"
        When I fill in "inputUserName" with "<username>"
        When I press "Apply"
        Then I should see "<response>"

        Examples:
            | tournament        | username      | response                      |
            |                   |               | This field is required        |
            | southcon_2095     |               | This field is required        |
            | conquest_2095     | bud           | Check username and tournament |
            | conquest_2095     | stevemcqueen  | Application submitted         |
            | southcon_2095     | stevemcqueen  | Application submitted         |
            | conquest_2095     | stevemcqueen  | You've already applied to conquest_2095    |
            | northcon_2095     | stevemcqueen  | northcon_2095 clashes with southcon_2095   |

#    Scenario: I sign up to a clashing tournament deliberately
#        Given I am on "/registerforatournament"
#        When I select "northcon_2095" from "inputTournamentName"
#        When I fill in "inputUserName" with "Jerry"
#        When I press "Apply"
#        Then I should see "northcon_2095 clashes with southcon_2095"
#        When I press "Apply Anyway!"
#        Then I should see "Application Submitted"

