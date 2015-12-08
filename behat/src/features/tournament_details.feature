Feature: Get information about a tournament
    I want to get info about a tournament
    As a prospective player
    So that I can apply to the enter

    Scenario: Want info about northcon_2095
        Given I am on "/tournament/northcon_2095"
        Then I should see "Name: northcon_2095"
        Then I should see "Date: 2095-06-01"
        Then I should see "Apply to play in northcon_2095"

    Scenario: I try to enter a tournament from the page
        Given I am on "/tournament/northcon_2095"
        Then I press "Apply to play in northcon_2095"
        Then I should be on "/login?next=/registerforatournament"
        When I fill in "id_inputUsername" with "charlie_murphy"
        When I fill in "id_inputPassword" with "darkness"
        When I press "Login"
        Then I should be on "/registerforatournament"
        When I select "northcon_2095" from "inputTournamentName"
        When I fill in "inputUserName" with "charlie_murphy"
        When I press "Apply"
        Then I should see "Application submitted"
        Given I am on "/tournament/northcon_2095"
        Then I press "Apply to play in northcon_2095"
        Then I should be on "/registerforatournament"
        When I select "northcon_2095" from "inputTournamentName"
        When I fill in "inputUserName" with "charlie_murphy"
        When I press "Apply"
        Then I should see "You've already applied to northcon_2095"

    Scenario: I try to visit a non-existent page
        Given I am on "/tournament/not_a_tournament"
        Then I should see "Tournament not_a_tournament not found in database"

    Scenario: I check the API for information on northcon_2095
        Given I GET "/tournamentDetails/northcon_2095" from the API
        Then the response is JSON
        Then the response has a "name" property

    Scenario: I check the API for information on not_a_tournament
        When I GET "/tournamentDetails/not_a_tournament" from the API
        Then the API response status code should be 400

